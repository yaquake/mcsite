from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import Contact, NewsForm
from .models import News, Person, Property, Services
from django.core.paginator import Paginator
import facebook
from .tasks import send_email_task
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def home(request):
    news = News.objects.all().order_by('-pub_date')[:7]
    # graph = facebook.GraphAPI(access_token="EAAE2SwiAhjABAHEllR19CJFA4LwWRVuUMTzp4MgX7ObA7Ubaz52z1AuFHEmmvgcQkNGHwyBeNxA4cQxBlqLm3AV43nZBNcOlAFFvkxtUhzsNZB4DKCZCLGLptfNZBoT6w7VYqWLcOIg66I53Y7eGSa8OuQt1t767f71zpgGhVxds50NubNcHLT8sPi5mETvoV7wZCVklnIaHgT5y4KiciD9h7qWfINzs1aLZA8KvG9ZBgZDZD")
    # print(graph)
    # attachment = {
    #     'name': 'Link name',
    #             'link': 'https://www.example.com/', 'caption': 'Check out this example',
    # 'description': 'This is a longer description of the attachment'}
    # # feed = graph.get_connections("me", "feed")
    # graph.put_object('me', 'feed', message='Hello, world!')
    return render(request, 'index.html', {'home': 'HOME', 'news': news, 'page': 1})


def services(request):
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})


def login(request):
    if request.method == 'POST':
        try:
            user1 = User.objects.get(username=request.POST['login'])
            user = auth.authenticate(username=user1.username, password=request.POST['password'])
            if user:
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Wrong credentials'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Wrong credentials'})
    else:
        return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


# @cache_page(CACHE_TTL)
def properties(request, page):
    property = Property.objects.all()
    paginator = Paginator(property, 9)
    list_count = len(property)
    result = paginator.page(page)
    return render(request, 'properties.html', {'list_count': list_count, 'result': result})


def property_details(request, key):
    property = get_object_or_404(Property, code=key)
    return render(request, 'property_details.html', {'property': property})


def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            body_text = 'From: {}\n\nPh: {}\n\nQuestion: {}'.format(form.cleaned_data['email'],
                                                                    form.cleaned_data['phone'],
                                                                    form.cleaned_data['details'])
            send_email_task.delay(form.cleaned_data['topic'],
                                  body_text,
                                  form.cleaned_data['email'],
                                  )
            return redirect('home')
    form = Contact()
    return render(request, 'contact.html', {'form': form})


@cache_page(CACHE_TTL)
def apply(request):
    return render(request, 'apply.html')


def about(request):
    personnel = Person.objects.all()
    return render(request, 'about.html', {'personnel': personnel})


@login_required()
def postnews(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        news_form = NewsForm()
        return render(request, 'add_news.html', {'form': news_form})


def news(request, page):
    news = News.objects.all().order_by('-pub_date')
    paginator = Paginator(news, 10)
    result = paginator.page(page)
    return render(request, 'news.html', {'news': result})


def news_details(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news_details.html', {'news': news})

