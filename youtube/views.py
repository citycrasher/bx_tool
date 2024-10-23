from django.shortcuts import render
from django.db.utils import IntegrityError
from . import youtube_API
from .forms import Youtube_whitelist_form
from .models import Client, youtube_whitelist, Youtube_Url_Model
from accounts.models import User_url_report
from .validators import check_youtube_urls
import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


@login_required
def home_view(request):
    return render(request=request, template_name='home.html')

@login_required
def search(request):
    if request.method == "GET":
        search_key = request.GET.get('key')
        video_url_result = Youtube_Url_Model.objects.filter(video_url__contains=search_key)
        # channel_url_result = Youtube_Url_Model.objects.filter(channel_url__contains=search_key)
        # channel_name_result = Youtube_Url_Model.objects.filter(channel_name__contains=search_key)
        # content_title_result = Youtube_Url_Model.objects.filter(content_title__contains=search_key)

        context = {'search_key': search_key, "video_url_result":video_url_result}
        return render(request=request, template_name="search_result_view.html", context=context)

# internal use
def check_youtube_whitelist(channel_id):
    if youtube_whitelist.objects.filter(channel_id=channel_id).exists():
        return True
    else:
        return False

# internal use
def check_url_to_db(request, video_url, video_detail):
    if Youtube_Url_Model.objects.filter(video_url=video_url).exists():
        return True
    else:
        # adding url to db
        Youtube_Url_Model(channel_url=video_detail['snippet']['channelId'],
                          upload_date= video_detail['snippet']['publishedAt'],
                          content_title=video_detail['snippet']['title'] ,
                          views=video_detail['statistics']['viewCount'],
                          channel_name= video_detail['snippet']['channelTitle'],
                          channel_sub_count= video_detail['channel_details']['subscriberCount'],
                          content_duration= video_detail['contentDetails']['duration'],
                          video_url=video_url, added_by=request.user).save()
        return False

# internal use
def report_user_result(request, new=0, duplicate=0, whitelisted=0, invalid_url=0):
    obj, status = User_url_report.objects.get_or_create(user=request.user)
    obj.new = obj.new + new
    obj.duplicate = obj.duplicate + duplicate
    obj.whitelisted = obj.whitelisted + whitelisted
    obj.invalid_url = obj.invalid_url + invalid_url
    obj.save()

@login_required
def youtube_filter(request):
    final_results = []
    white_listed_result = []
    duplicate_result = []
    new_results = []
    invalid_results = []
    if request.method == "POST":
        youtube_urls = request.POST.get('input_urls')
        for url in set(str(youtube_urls).split()):
            # https://www.youtube.com/watch?v=-Sz4rKmQESg
            if "youtube.com" in url and 'v=' in url:
                video_details = youtube_API.get_video_details(url.split("=")[1])
                video_id = video_details.get('id', None)
                if video_id:
                    channel_id = video_details['snippet']['channelId']
                    # check url is already exists or not
                    if check_url_to_db(request, video_url=f'https://www.youtube.com/watch?v={video_id}', video_detail=video_details):
                        duplicate_result.append(video_details)
                    else:
                        # checking the youtube whitelist
                        if check_youtube_whitelist(channel_id):
                            white_listed_result.append(video_details)
                        else:
                            new_results.append(video_details)
                else:
                    invalid_results.append({url: "invalid_url"})
            else:
                invalid_results.append({url:"invalid_url"})
        # storing user results in db
        report_user_result(request, new=len(new_results), duplicate=len(duplicate_result),
                           whitelisted=len(white_listed_result), invalid_url=len(invalid_results))
        user_stat = {"new":len(new_results), "duplicate":len(duplicate_result), "white_list":len(white_listed_result), "invalid":len(invalid_results)}
        context = {"Infringing_results": new_results, "whitelist_result": white_listed_result,
                   "invalid_result": invalid_results, "duplicate_result" : duplicate_result , "user_stat":user_stat}
        return render(request=request, template_name='youtube/youtube_filter_results.html', context=context)
    #return render(request=request, template_name='youtube/youtube_filter_results.html')
    return render(request=request, template_name='youtube/youtube_form.html')

def get_whitelist_urls_from_file(file):
    file_contents = file.read().decode('utf-8')
    return file_contents.split()


@login_required
def youtube_add_whitelist(request):
    context = {}
    valid_url_list = []
    invalid_url_list = []
    channel_url_list = None
    invalid_data = None
    if request.method == "POST":
        client = request.POST.get('client')
        channel_url = request.POST.get('input_urls')
        file = request.FILES.get("csv_file", None)
        if channel_url and client != 'Select Client':
            channel_url_list = channel_url.split()
        elif file and client != 'Select Client':
            channel_url_list = get_whitelist_urls_from_file(file)
        else:
            invalid_data = True
        if channel_url_list:
            # getting client object
            client_obj = Client.objects.get(pk=client)
            # Seperating url into valid and invalid urls
            valid_url_list, invalid_url_list = check_youtube_urls(channel_url_list)
            if len(valid_url_list) > 0:
                for url in valid_url_list:
                    # Youtube API Call get channel details
                    channel = youtube_API.get_channel_details_from_url(url=url)
                    if channel:
                        # check the data is already present in db or not
                        try:
                            obj, created = youtube_whitelist.objects.get_or_create(channel_title=channel['channel_title'],
                                                                                   channel_id=channel['channel_id'],
                                                                                   channel_url=channel['channel_url'],
                                                                                   client=client_obj,
                                                                                   added_by=request.user)
                            print("++ data", obj, created)
                        except IntegrityError as e:
                            print("Integrity Error")
                    else:
                        valid_url_list.remove(url)
                        invalid_url_list.append(url)
    client_data = Client.objects.all()
    context = {"clients": client_data, 'valid_url_count':len(valid_url_list), 'invalidUrl_list':invalid_url_list}
    if invalid_data:
        context['invalid_data'] = invalid_data
    #print("final context", context)
    return render(request=request, template_name='youtube/youtube_whitelist_form.html', context=context)

@login_required
def Client_list_view(request):
    client_list = Client.objects.all()
    return render(request=request, template_name='client/client_list_view.html', context={'clients': client_list})

@login_required
def Client_based_whitelist_view(request, client):
    client_obj = Client.objects.get(client_name=client)
    whitelist_results = youtube_whitelist.objects.filter(client=client_obj.pk)
    context = {'client': client, 'whitelist_results' : whitelist_results}
    return render(request=request, template_name='client/client_based_whitelist_view.html', context=context)

@login_required
def Client_Whitelist_Download_CSV(request, client):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{client}.csv"'.format(client=client)
    writer = csv.writer(response)
    client_obj = Client.objects.get(client_name=client)
    whitelist_results = youtube_whitelist.objects.filter(client=client_obj.pk)

    writer.writerow(['Title', 'Id', 'Url', 'Client', 'Added By' ])
    for result in whitelist_results:
        writer.writerow([result.channel_title, result.channel_id, result.channel_url, result.client, result.added_by])
    return response


@login_required
def add_client_view(request):
    if request.method == "POST":
        client = request.POST.get('client_name')
        obj, created =Client.objects.get_or_create(client_name=client)
        if created:
            context = {"positive_Notification_data": obj}
        else:
            context = {"negative_Notification_data": obj}
        return render(request=request, template_name='client/add_client_form.html', context=context)
    return render(request=request, template_name='client/add_client_form.html')