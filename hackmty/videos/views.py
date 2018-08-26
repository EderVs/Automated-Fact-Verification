from django.shortcuts import render
from django.http import HttpResponse

from . import utils, audio, search

def index(request):
    template = "videos/index.html"
    context = {}
    return render(request, template, context)

def video(request):

    url = request.GET.get("url", '')
    start_min = 0
    start_sec = 0
    end_min = 0
    end_sec = 10

    text = audio.get_text_from_video(url, start_min, start_sec, end_min, end_sec)
    results = search.search(text)

    video = {}
    video['url'] = utils.get_embed(request.GET.get('url', ''))
    video['text'] = text
    video['results'] = results
    template = "videos/video.html"
    context = {'video': video}
    return render(request, template, context)

