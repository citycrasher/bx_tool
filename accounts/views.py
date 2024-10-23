from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import  User_url_report
from django.contrib.auth import authenticate
from django.http import HttpResponse

# Create your views here.
@login_required
def User_report_view(request):
    try:
        data = User_url_report.objects.get(user=request.user)
    except:
        data = {}
    return render(request=request, template_name='user/UserReport.html', context={'user_stat': data})

@login_required
def ChangePassword(request):
    context ={}
    if request.method == 'POST':
        currentPassword =  str(request.POST.get('CurrentPassword'))
        newPassword = str(request.POST.get('NewPassword'))
        confirmPassword = str(request.POST.get('ConfirmPassword'))
        print(currentPassword, newPassword, confirmPassword)
        auth = authenticate(username=request.user.username, password=currentPassword)
        if auth is not None:
            if newPassword == confirmPassword:
                user = request.user
                user.set_password(newPassword)
                user.save()
                # Re-authenticate the user to maintain the session
                # update_session_auth_hash(request, user)
                return redirect("accounts:login")
            else:
                context = {'error_msg' : "New password and Confirm password are not same"}
        else:
            context = {'error_msg' : "Current password is incorrect"}

    return render(request=request, template_name='auth/ResetPassword.html', context=context)

def ForgotPassword(request):
    return render(request=request, template_name='auth/auth-forgot-password.html')