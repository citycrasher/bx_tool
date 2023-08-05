from django import forms
from .models import youtube_whitelist

class Youtube_whitelist_form(forms.ModelForm):
    class Meta:
        model = youtube_whitelist
        fields = [
            "channel_title",
            "channel_id",
            "channel_url",
            "client",
        ]