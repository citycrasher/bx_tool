import requests

#internal_use
def is_youtube_url(url):
    """Check if a URL is a valid YouTube URL."""
    return "youtube.com" in url or "youtu.be" in url

def check_youtube_urls(urls):
    valid_url = []
    invalid_url = []
    """Check if a list of URLs are valid and related to YouTube."""
    for url in set(urls):
        try:
            # Check if the URL is valid
            response = requests.get(url)
            response.raise_for_status()

            # Check if the URL is related to YouTube
            if is_youtube_url(url):
                valid_url.append(url)
            else:
                invalid_url.append(url)
        except requests.exceptions.RequestException:
            invalid_url.append(url)
    return valid_url, invalid_url
