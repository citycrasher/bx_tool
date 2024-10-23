import time
from django.urls import reverse
from django.shortcuts import render, HttpResponse
from ip_reporting.decorators import custom_permission_required
from youtube.models import Client, Movie, AppConfig, IP_Report
from django.db.models import Count

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bx_tools.utils import get_urls_from_file
from . import fb_api
from bx_tools import export
from .models import ApprovedMetaDomain
from urllib.parse import urlparse
from accounts.models import User_url_report

#internal Use
def check_duplicate(urlList):
    newUrl = []
    duplicateUrl = []
    # Get all report URLs that match the URLs in the list
    existing_reports = set(IP_Report.objects.filter(report_url__in=urlList).values_list('report_url', flat=True))
    # Check if any URL in the list already exists in the database
    for url in urlList:
        if url in existing_reports:
            duplicateUrl.append(url)
        else:
            newUrl.append(url)
    return newUrl, duplicateUrl

#internal Use
def update_user_stats(request, new=0, duplicate=0, invalid_url=0):
        obj, status = User_url_report.objects.get_or_create(user=request.user)
        obj.meta_new = obj.meta_new + new
        obj.meta_deplicate = obj.meta_deplicate + duplicate
        obj.meta_invalid = obj.meta_invalid + invalid_url
        obj.save()

#internal Use
def is_url_in_approved_domains(url, approved_domains):
    domain = urlparse(url).netloc
    print(domain,"++++++++++++")

    return domain in approved_domains

#internal use
def check_url(urlList):
    approvedList = []
    unApprovedUrlList = []
    urls = urlList.split()
    approvedDomainList  = str(ApprovedMetaDomain.objects.get().approvedDomain).split(",")

    for url in urls:
        if is_url_in_approved_domains(url, approvedDomainList):
            approvedList.append(url)
        else:
            unApprovedUrlList.append(url)
    return approvedList, unApprovedUrlList

@custom_permission_required("can_access_custom_permission")
def ip_reporting_facebook(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request=request, template_name='ip_reporting_form.html', context=context)

def common_ip_reporting(request):
    if request.method == 'POST':
        print("data recived")
        ownderName = request.POST.get("OwnerName")
        MovieName = request.POST.get("MovieName")
        original_type = request.POST.get("original_type")
        originalUrl = request.POST.get("originalUrl")
        if 'file' in request.FILES:
            file = request.FILES['file']
            urlList = get_urls_from_file(file)
        else:
            urlList = request.POST.get("input_urls", None)

        approvedUrlList, invalidUrlList = check_url(urlList)
        urlList, duplicate = check_duplicate(approvedUrlList)
        update_user_stats(request=request, new=len(urlList), duplicate=len(duplicate), invalid_url=len(invalidUrlList))

        try:
            response, status_code = general_call_api(urlList, MovieName, ownderName, originalUrl, original_type)
            print("requested")
            with open("meta.txt", "a") as file:
                file.write(f"{response} -- {status_code}")
        except Exception as e:
            return render(request=request, template_name='common_ip_reporting_form.html')
    return render(request=request, template_name='common_ip_reporting_form.html')


@csrf_exempt  # This is to simplify, but not recommended for production without further security measures
def ajax_get_movies_list(request):
    client_id = request.GET.get('client_id')
    movies = Movie.objects.filter(client_id=client_id).values('id', 'movie_name')
    return JsonResponse(list(movies), safe=False)

def update_ip_report_db(movieObj,original_type, urlList, status, response=None):
    if response:
        reports = [IP_Report(client=movieObj.client, movie=movieObj, report_url=url, original_type=original_type,
                             status=status, report_id=response["report_id"], request_id=response["id"]) for url in urlList]
    else:
        reports = [IP_Report(client=movieObj.client, movie=movieObj, report_url=url,
                             original_type=original_type) for url in urlList]
    IP_Report.objects.bulk_create(reports)

@csrf_exempt
def ajax_post_form_ip_report(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            urlList = get_urls_from_file(file)
        else:
            urlList = request.POST.get('url')
        approvedUrlList, invalidUrlList = check_url(urlList)
        urlList, duplicate = check_duplicate(approvedUrlList)
        update_user_stats(request=request, new=len(urlList), duplicate= len(duplicate), invalid_url=len(invalidUrlList))
        urlList = "\n".join(urlList) # convert back into string
        movie = request.POST.get('movie')
        original_type = request.POST.get('original_type')
        movieObj = Movie.objects.get(id=int(movie))
        try:
            response, status_code = call_api(urlList, movieObj, original_type)
            update_ip_report_db(movieObj, original_type, str(urlList).split(), 'REPORTED',response)
        except Exception as e:
            update_ip_report_db(movieObj,original_type, str(urlList).split(), 'PENDING')
        return JsonResponse({'data': 'success request'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def general_call_api(raw_urls, movieName, ownerName, original_work_url, original_type):
    appObj = AppConfig.objects.get(id=1)
    movie_name = movieName
    access_token = (
        "EAANNzoa1UqQBOwv6fqRZB4R9LZAVih8rXyKJeuqB9wNXyQNeTC4Kp4xLTNpDGSjiEQPVlF2AuZCSG966BFLXjZCQBsxmLG4up66dr3123ywiOT9ZAJOCWw6OHPOJCGQBLHvbuuhyMY1gJyMy0FX3HHcQaJwz3LnTNW5xuA8JLW9cS9jgXi5ZCH2azsMQZDZD")
    email = appObj.company_legal_email
    #job = "Legal Operations"
    job = "TEST"
    name = appObj.company_name
    original_type = original_type  # PHOTO, VIDEO, ARTWORK, SOFTWARE, NAME, CHARACTER, OTHER
    owner_country = 'IN'  # IN-india,
    owner_name =  ownerName # client name
    relationship = "AGENT"  # OWNER, COUNSEL, EMPLOYEE, AGENT, OTHER
    type = "COPYRIGHT"  # COPYRIGHT, TRADEMARK, COUNTERFEIT
    content_urls = raw_urls
    organization = appObj.company_name
    address = appObj.company_address
    original_urls = original_work_url

    additional_info = fb_api.get_additional_info(movie_name)

    if appObj.environment == "DEV":
        print("DEV")
        job = "TEST"
        email = "city.crasher1@gmail.com"
    data = fb_api.get_data(access_token=access_token, email=email, job=job, name=name, original_type=original_type,
                        owner_country=owner_country, owner_name=owner_name, relationship=relationship, type=type,
                        organization=organization, address=address, original_urls=original_urls,
                        content_urls=content_urls, additional_info=additional_info)

    response = fb_api.make_request(data)
    return response.json(), response.status_code


def call_api(raw_urls, movieObj, original_type ):
    appObj = AppConfig.objects.get(id=1)
    movie_name = movieObj.movie_name
    access_token = (
        "EAANNzoa1UqQBO40zbflEj38R7AZBa7FcLthmSfEgXQyq8AKa4sBucsVJZBDmwXVF17oiQTCyeXdWnVUdiFRTPqolxeu9keCOPFwKnXkZCHvTMh0oLDahJUagxaPOy4ZBQ7uZBrrzBp0RZARt5nzvJH0odjSEQvF3XnOQWJgU9vDzCQNZARNsSimh7RE5QZDZD")
    email = appObj.company_legal_email
    #job = "Legal Operations"
    job = "TEST"
    name = appObj.company_name
    original_type = original_type  # PHOTO, VIDEO, ARTWORK, SOFTWARE, NAME, CHARACTER, OTHER
    owner_country = movieObj.client.client_country  # IN-india,
    owner_name = movieObj.client.client_name  # client name
    relationship = "AGENT"  # OWNER, COUNSEL, EMPLOYEE, AGENT, OTHER
    type = "COPYRIGHT"  # COPYRIGHT, TRADEMARK, COUNTERFEIT
    content_urls = raw_urls
    organization = appObj.company_name
    address = appObj.company_address
    original_urls = movieObj.original_work

    additional_info = fb_api.get_additional_info(movie_name)

    if appObj.environment == "DEV":
        print("DEV")
        job = "TEST"
        email = "city.crasher1@gmail.com"
    data = fb_api.get_data(access_token=access_token, email=email, job=job, name=name, original_type=original_type,
                        owner_country=owner_country, owner_name=owner_name, relationship=relationship, type=type,
                        organization=organization, address=address, original_urls=original_urls,
                        content_urls=content_urls, additional_info=additional_info)

    response = fb_api.make_request(data)
    return response.json(), response.status_code

def ajax_get_report_forMovie(request):

    movie = request.GET.get("movie_id")
    # Retrieve parameters sent by DataTables
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 100))

    # Get the total number of records
    total_records = IP_Report.objects.count()

    # Apply pagination and retrieve the requested slice of data
    results = IP_Report.objects.filter(movie=int(movie)).values('report_url', 'original_type', 'status','report_id', 'request_id')

    # Construct the response
    response = {
        "draw": draw,
        "recordsTotal": total_records,
        "recordsFiltered": total_records,
        "data": list(results),
    }

    return JsonResponse(response)


def ip_report_form_view(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request=request, template_name="report/ip_report1.html", context=context) #TODO change the template name later to form


def ip_report_result_view(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        query_set = IP_Report.objects.filter(movie_id=movie_id).values('client__client_name', 'report_url', 'original_type', 'report_id',
                                                                        'request_id','status','time_stamp')
        movie_obj = Movie.objects.get(id=movie_id)
        context = {"datas": query_set, "movie_obj": movie_obj }
        return render(request=request, template_name="utils/content_test_table_duplicate.html", context=context)

def export_file(request, export_type, id):
    data_set = IP_Report.objects.filter(movie_id=int(id))
    status_counts = data_set.values('status').annotate(count=Count('status'))

    # Prepare data and labels for the chart
    labels = [item['status'] for item in status_counts]
    data = [item['count'] for item in status_counts]
    movie_obj = Movie.objects.get(id=int(1))
    context = {"datas": data_set, "movie_obj": movie_obj,
               'labels': labels, "data_point": data
               }
    if export_type == 'pdf':
        return export.generate_pdf(context)
    elif export_type == 'csv':
        return export.generate_csv(context)
    elif export_type == 'excel':
        return export.generate_excel(context)
    elif export_type == 'copy':
        pass
    elif export_type == 'print':
        return export.generate_print()

def table_test(request):
    data_set = IP_Report.objects.filter(movie_id=int(1))
    status_counts = data_set.values('status').annotate(count=Count('status'))

    # Prepare data and labels for the chart
    labels = [item['status'] for item in status_counts]
    data = [item['count'] for item in status_counts]

    movie_obj = Movie.objects.get(id=int(1))
    context = {"datas": data_set, "movie_obj": movie_obj,
               'labels': labels, "data_point":data
               }
    return render(request=request, template_name="export/exportPDF.html", context=context)