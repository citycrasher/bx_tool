"""
URL configuration for bx_tools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'youtube'
urlpatterns = [
    path('', views.home_view, name="home_view"),
    path('youtube', views.youtube_filter, name="youtube_filter"),
    path('youtube_add_whitelist', views.youtube_add_whitelist, name="youtube_add_whitelist"),
    path('client_list_view', views.Client_list_view, name="client_list_view"),
    path('client_based_whitelist/<str:client>', views.Client_based_whitelist_view, name='client_based_whitelist'),
    path('client_whitelist_csv_download/<str:client>', views.Client_Whitelist_Download_CSV, name='client_whitelist_csv_download'),



    path('add_client_view', views.add_client_view, name='add_client_view'),

    path('search/', views.search, name='search')
]
