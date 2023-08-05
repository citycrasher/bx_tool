from googleapiclient.discovery import build
import isodate

api_key = 'AIzaSyCqs1gKxoezwa4Nt0xwTo3uvlIA7_BwGaQ'

def get_channel_id(videoID=None):
    youtube = build('youtube', 'v3', developerKey=api_key)
    if videoID:
        video_response = youtube.videos().list(part='snippet', id=videoID).execute()
        channel_id = video_response['items'][0]['snippet']['channelId']
    return channel_id

def get_video_details(videoID=None):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        if videoID:
            video_response = youtube.videos().list(part='statistics,snippet,contentDetails', id=videoID).execute()
            video_detail = video_response['items'][0]
            channel_id = video_response['items'][0]['snippet']['channelId']
            channel_details_response = youtube.channels().list(part='statistics', id=channel_id).execute()
            video_detail['channel_details'] = channel_details_response['items'][0]['statistics']
            content_duration = video_detail['contentDetails']['duration']
            video_detail['contentDetails']['duration'] = isodate.parse_duration(content_duration).total_seconds()
            print(content_duration)
            print(video_detail)
        return video_detail
    except Exception as e:
        return {videoID: e}


def get_channel_details_from_url(url):
    # custom name
    if '@' in url:
        custom_name = str(str(url).split("@")[1]).split('/')[0]
        print("sustome name", custom_name)
        channel_details = get_channel_details_from_custom_name(custom_name)
    elif 'user/' in url:
        name = str(str(url).split('user/')[1]).split("/")[0]
        channel_details = get_channel_details_from_custom_name(name)
    elif 'channel/' in url:
        id = str(str(url).split('channel/')[1]).split('/')[0]
        channel_details = get_channel_details_from_channel_id(id)
    elif 'watch?v=' in url:
        vidoe_id = str(str(url).split('watch?v=')[1]).split('/')[0]
        channel_details = get_channel_details_from_video_id(vidoe_id)
        # get data from video id
    return channel_details

# internal use
def get_channel_details_from_video_id(video_id):
    try:
        temp = dict()
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='id,snippet', id=video_id).execute()
        channel_id = video_response['items'][0]['snippet']['channelId']
        temp['channel_url'] = 'https://www.youtube.com/channel/{channelId}'.format(channelId = channel_id)
        temp['channel_title'] = video_response['items'][0]['snippet']['channelTitle']
        temp['channel_id'] = channel_id
        return temp
    except Exception as e:
        return False

# internal use
def get_channel_details_from_custom_name(custom_name):
    try:
        temp = dict()
        youtube = build("youtube", "v3", developerKey=api_key)
        # Call the YouTube API to retrieve the channel ID from the custom URL
        channels_response = youtube.channels().list(part='id,snippet', forUsername=custom_name).execute()
        print(channels_response)
        # Extract the channel ID from the API response
        channel_id = channels_response['items'][0]['id']
        temp['channel_id'] = channel_id
        temp['channel_url'] = 'https://www.youtube.com/channel/{channelId}'.format(channelId=channel_id)
        temp['channel_title'] = channels_response['items'][0]['snippet']['title']
        return temp
    except Exception as e:
        print("+++")
        print(e)
        return False

# internal use
def get_channel_details_from_channel_id(channel_id):
    temp = dict()
    youtube = build("youtube", "v3", developerKey=api_key)
    channel_response = youtube.channels().list(
        part='snippet',
        id=channel_id
    ).execute()
    try:
        channel_id = channel_response['items'][0]['id']
        temp['channel_id'] = channel_id
        temp['channel_url'] = 'https://www.youtube.com/channel/{channelId}'.format(channelId=channel_id)
        try:
            temp['channel_title'] = channel_response['items'][0]['snippet']['channelTitle']
        except KeyError:
            temp['channel_title'] = channel_response['items'][0]['snippet']['title']
        return temp
    except Exception as e:
        print(e)
        return dict()
