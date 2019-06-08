from .models import News
from django.core.paginator import Paginator
from .forms import NewsForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    DetailView
)


# post news
class PostNewsView(CreateView):
    template_name = 'add_news.html'
    form_class = NewsForm

    def get_success_url(self):
        return reverse('news', kwargs={'page': 1})


# List of news
class NewsListView(ListView):
    template_name = 'news.html'

    def get_queryset(self, ):
        news = News.objects.all().order_by('-pub_date')
        paginator = Paginator(news, 10)
        page_ = self.kwargs.get('page')
        return paginator.page(page_)


# Every news details
class NewsDetailView(DetailView):
    template_name = 'news_details.html'

    def get_object(self, queryset=None):
        slug_ = self.kwargs.get('slug')
        return get_object_or_404(News, slug=slug_)
