from django.contrib import admin
from .models import *
# Register your models here.


class youtube_whitelist_admin_view(admin.ModelAdmin):
    list_display = ('channel_title', 'channel_url', 'channel_id', 'client')
    search_fields = ['channel_title', 'channel_url', 'channel_id', 'client']


admin.site.register(youtube_whitelist, youtube_whitelist_admin_view)

class client_admin_view(admin.ModelAdmin):
    list_display = ('client_name',)
    search_fields = ['client_name']

admin.site.register(Client, client_admin_view)


admin.site.register(Youtube_Url_Model)
admin.site.register(Services)
admin.site.register(Movie)
admin.site.register(AppConfig)
admin.site.register(IP_Report)
