from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
# Create your tests here.
app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('User_report', views.User_report_view, name='User_report'),
]
