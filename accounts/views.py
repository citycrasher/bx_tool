from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from youtube.models import User_url_report

# Create your views here.
@login_required
def User_report_view(request):
    try:
        data = User_url_report.objects.get(user=request.user)
    except:
        data = {}
    return render(request=request, template_name='user/UserReport.html', context={'user_stat': data})