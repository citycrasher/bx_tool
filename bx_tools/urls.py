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
from django.conf.urls import handler403, handler404
from django.shortcuts import render
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('youtube.urls')),   # youtube
    path('accounts/', include('accounts.urls')),   # accounts
    path('ip_reporting/', include('ip_reporting.urls')) # IP reporting
]

# Define a view for the 403 error
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)



# Set the handler
handler403 = custom_permission_denied_view
handler404 = custom_404_view

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# print(static(settings.STATIC_URL, document_root=[settings.STATIC_ROOT]))