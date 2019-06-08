from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    PostNewsView,
    NewsListView,
    NewsDetailView
)

app_name = 'news'
urlpatterns = [
    path('postnews/', login_required(login_url='login')(PostNewsView.as_view()), name='postnews'),
    path('page<int:page>/', NewsListView.as_view(), name='news'),
    path('<str:slug>/', NewsDetailView.as_view(), name='news_details'),
]
