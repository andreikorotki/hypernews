from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('news/', views.news, name='news'),
    path('news/<int:link>/', views.news_item),
    path('news/create/', views.create_news_item),
]


urlpatterns += static(settings.STATIC_URL)
