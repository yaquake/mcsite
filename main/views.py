import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import Contact, NewsForm, Appraisal
from .models import News, Person, Property, Services, MainPageInfo, About, ContactUs, WhyUs, Guide
from django.core.paginator import Paginator
from .tasks import send_email_task
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.contrib import messages

# TimeToLive of redis cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def recaptcha(post):
    recaptcha_response = post
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result['success']


def home(request, success_message=None):
    newsfeed = News.objects.all().order_by('-pub_date')[:6]
    main_page_info = MainPageInfo.objects.first()
    return render(request, 'index.html', {'home': 'HOME',
                                          'news': newsfeed,
                                          'page': 1,
                                          'info': main_page_info})


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
def listings(request, page):

    property = Property.objects.all()
    paginator = Paginator(property, 9)
    list_count = len(property)
    result = paginator.page(page)
    return render(request, 'listings.html', {'list_count': list_count, 'result': result})


# Property details of every property
@cache_page(CACHE_TTL)
def property_details(request, key):
    property = get_object_or_404(Property, code=key)
    return render(request, 'property_details.html', {'property': property})


# Contact page with reCaptcha v3 validation
def contact(request):
    form = Contact()
    contact_info = ContactUs.objects.first()
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            if recaptcha(request.POST['g-recaptcha-response']):
                body_text = 'From: {}, {}\n\nPh: {}\n\nQuestion: {}'.format(form.cleaned_data['name'], form.cleaned_data['email'],
                                                                            form.cleaned_data['phone'],
                                                                            form.cleaned_data['details'])
                send_email_task.delay(form.cleaned_data['topic'],
                                      body_text,

                                      )
                form = Contact()
                messages.success(request, 'Your message has been sent.')

            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        else:
            return render(request, 'contact.html', {'error': 'The data you have entered is invalid', 'form': form,
                                                    'contact': contact_info})

    return render(request, 'contact.html', {'form': form, 'contact': contact_info})


# Apply tenancy page
@cache_page(CACHE_TTL)
def apply(request):
    return render(request, 'apply.html')


# About page
def about(request):
    personnel = Person.objects.all().order_by('pk')
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


def send_appraisal(request):
    appraisal = Appraisal()
    if request.method == 'POST':
        form = Appraisal(request.POST)
        if form.is_valid():
            if recaptcha(request.POST['g-recaptcha-response-2']):

                body_text = 'From: {}, {}\n\nPh: {}\n\nAddress: {}, {}, {}\n\nBedrooms: {}\n\nBathrooms:' \
                            ' {}\n\nCarparks: {}\n\nDetails: {}'.format(
                                                                        form.cleaned_data['name'],
                                                                        form.cleaned_data['email'],
                                                                        form.cleaned_data['phone'],
                                                                        form.cleaned_data['street_address'],
                                                                        form.cleaned_data['suburb'],
                                                                        form.cleaned_data['postcode'],
                                                                        form.cleaned_data['bed'],
                                                                        form.cleaned_data['bath'],
                                                                        form.cleaned_data['car'],
                                                                        form.cleaned_data['details'])
                send_email_task.delay('Free rental appraisal',
                                      body_text,

                                      )
                form = Appraisal()
                messages.success(request, 'Your message has been sent.')

            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        else:
            return render(request, 'appraisal.html', {'error': 'The data you have entered is invalid',
                                                      'form': appraisal})

    return render(request, 'appraisal.html', {'form': appraisal})


def whyus(request):
    why = WhyUs.objects.first()
    return render(request, 'whyus.html', {'why': why})


def tenancy(request):
    guide = Guide.objects.first()
    return render(request, 'guide.html', {'guide': guide})

