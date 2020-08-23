from datetime import date, datetime
from django.shortcuts import render
from django.conf import settings
import json
from django import forms
from django.shortcuts import redirect
import time


def get_all_news():
    with open(settings.NEWS_JSON_PATH, 'r') as news_file:
        news_all = json.load(news_file)
    return news_all


def write_news_item(news_item):
    news_all = get_all_news()
    news_all.append(news_item)
    with open(settings.NEWS_JSON_PATH, 'w') as news_file:
        json.dump(news_all, news_file)


def get_news_by_link(link):
    news_array = []
    news_all = get_all_news()
    news_array = [x for x in news_all if x['link'] == link]
    return news_array


# Create your views here.
def index(request):
    return redirect('/news/')


def news(request):
    return render(request, 'news.html')


def news(request):
    news_all = get_all_news()
    for item in news_all:
        item['created_date'] = datetime.strptime(item.get('created'), '%Y-%m-%d %H:%M:%S').date()
    news_all.sort(key=lambda news_all: news_all['created_date'], reverse=True)

    return render(request, 'news.html', {'all_news': news_all})


def news_item(request, link):
    news_arr = get_news_by_link(link)
    return render(request, 'news_item.html', {'news': news_arr[0]})


class NewsForm(forms.Form):
    title = forms.CharField(label='title', max_length='1024')
    text = forms.CharField(label='text', max_length='4096')


def create_news_item(request, *args, **kwargs):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            text = request.POST.get('text')
            title = request.POST.get('title')
            news_item = {"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         "text": text,
                         "title": title,
                         "link": int(time.time())
                         }
            write_news_item(news_item)
            return redirect('/news/')
    # if a GET (or any other method) we'll create a blank form
    else:
        news_form = NewsForm()
        return render(request, 'news_create.html', {'news_form': news_form})
