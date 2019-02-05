from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import Contact, NewsForm
from .models import News, Person, Property, Services, MainPageInfo, About, ContactUs
from django.core.paginator import Paginator
from .tasks import send_email_task
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

# TimeToLive of redis cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def home(request):
    news = News.objects.all().order_by('-pub_date')[:7]
    main_page_info = MainPageInfo.objects.first()
    return render(request, 'index.html', {'home': 'HOME', 'news': news, 'page': 1, 'info': main_page_info})


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
    return render(request, 'login.html')


# Logout function
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


# List of properties
@cache_page(CACHE_TTL)
def properties(request, page):
    property = Property.objects.all()
    paginator = Paginator(property, 9)
    list_count = len(property)
    result = paginator.page(page)
    return render(request, 'properties.html', {'list_count': list_count, 'result': result})


# Property details of every property
def property_details(request, key):
    property = get_object_or_404(Property, code=key)
    return render(request, 'property_details.html', {'property': property})


# Contact page
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
    contact_info = ContactUs.objects.first()
    return render(request, 'contact.html', {'form': form, 'contact': contact_info})


# Apply tenancy page
@cache_page(CACHE_TTL)
def apply(request):
    return render(request, 'apply.html')


# About page
def about(request):
    personnel = Person.objects.all()
    about = About.objects.first()
    return render(request, 'about.html', {'personnel': personnel, 'about': about})


# post news
@login_required(login_url='login')
def postnews(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news', page=1)
    else:
        news_form = NewsForm()
        return render(request, 'add_news.html', {'form': news_form})


# List of news
def news(request, page):
    news = News.objects.all().order_by('-pub_date')
    paginator = Paginator(news, 10)
    result = paginator.page(page)
    return render(request, 'news.html', {'news': result})


# Every news details
def news_details(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news_details.html', {'news': news})

