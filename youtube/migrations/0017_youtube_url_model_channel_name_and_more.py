# Generated by Django 4.2.1 on 2023-07-08 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0016_alter_youtube_whitelist_channel_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtube_url_model',
            name='channel_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='youtube_url_model',
            name='channel_sub_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='youtube_url_model',
            name='channel_url',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='youtube_url_model',
            name='content_title',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AddField(
            model_name='youtube_url_model',
            name='upload_date',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='youtube_url_model',
            name='views',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='youtube_whitelist',
            name='channel_url',
            field=models.CharField(max_length=1500, unique=True),
        ),
    ]