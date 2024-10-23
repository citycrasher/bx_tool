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

app_name = 'ip_reporting'
urlpatterns = [
    path('reporting', views.ip_reporting_facebook, name="ip_reporting_view"),
    path('common_ip_reporting', views.common_ip_reporting, name="common_ip_reporting"),

    path('ajax_get_movies_list', views.ajax_get_movies_list, name="ajax_get_movies_list"),
    path('ajax_post_form_ip_report', views.ajax_post_form_ip_report, name="ajax_post_form_ip_report"),
    path('ip_report_view', views.ip_report_form_view, name="ip_report_view"),
    path('ip_report_result_view', views.ip_report_result_view, name="ip_report_result_view"),
    path('export_file/<export_type>/<id>', views.export_file, name="export_file"),

    path('test', views.table_test, name="test_table"),
    path('ajax_get_report_forMovie', views.ajax_get_report_forMovie, name="ajax_get_report_forMovie")
]
