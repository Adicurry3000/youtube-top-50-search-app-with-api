import requests
from isodate import parse_duration
from django.conf import settings
from django.shortcuts import render, redirect


def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        channel_url = 'https://www.googleapis.com/youtube/v3/channels'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 48,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []

        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0]}')

        video_prams = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet, contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 48,
        }

        r = requests.get(video_url, params=video_prams)

        results = r.json()['items']

        for result in results:

            video_data = {
                'title': result['snippet']['title'],
                'channel': result['snippet']['channelTitle'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"]}',
                'duration':parse_duration(result['contentDetails']['duration']),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }
            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'search/index.html', context)
