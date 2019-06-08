import requests
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf.urls.static import settings
from .forms import Contact, Appraisal
from news.models import News
from .models import MainPageInfo, Services, ContactUs, Person, WhyUs, About, Guide
from properties.tasks import send_email_task


def recaptcha(post):
    recaptcha_response = post
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    return result['success']


class Home(View):
    template_name = 'index.html'

    def get_queryset(self):
        newsfeed = News.objects.all().order_by('-pub_date')[:6]
        return newsfeed

    def get(self, request, *args, **kwargs):
        main_page_info = MainPageInfo.objects.first()
        context = {
            'object_list': self.get_queryset(),
            'page': 1,
            'info': main_page_info,
            'home': 'HOME',
        }

        return render(request, self.template_name, context)


class ServicesListView(ListView):
    template_name = 'services.html'
    queryset = Services.objects.all()


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            user1 = User.objects.get(username=request.POST['login'])
            user = auth.authenticate(username=user1.username, password=request.POST['password'])
            if user:
                auth.login(request, user)
                return redirect('home')
            else:
                return render(request, self.template_name, {'error': 'Wrong credentials'})
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'Wrong credentials'})


# Logout function
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        return reverse('home')


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        form = Contact()
        contact_info = ContactUs.objects.first()
        context = {
            'form': form,
            'contact': contact_info
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contact_info = ContactUs.objects.first()
        form = Contact(request.POST)
        if form.is_valid():
            if recaptcha(request.POST['g-recaptcha-response']):
                body_text = 'From: {}, {}\n\nPh: {}\n\nQuestion: {}'.format(form.cleaned_data['name'],
                                                                            form.cleaned_data['email'],
                                                                            form.cleaned_data['phone'],
                                                                            form.cleaned_data['details']
                                                                            )
                send_email_task.delay(form.cleaned_data['topic'],
                                      body_text
                                      )
                form = Contact()
                messages.success(request, 'Your message has been sent.')

            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        else:
            return render(request, self.template_name, {'error': 'The data you have entered is invalid', 'form': form,
                                                        'contact': contact_info})


# Apply tenancy page
class ApplyView(View):
    def get(self, request):
        return render(request, 'apply.html')


# About page
class AboutView(View):
    def get(self, request):
        personnel = Person.objects.all().order_by('pk')
        about = About.objects.first()
        context = {
            'personnel': personnel,
            'about': about
        }
        return render(request, 'about.html', context)


def why_us(request):
    why = WhyUs.objects.first()
    context = {
        'why': why
    }
    return render(request, 'whyus.html', context)


def tenancy(request):
    guide = Guide.objects.first()
    context = {
        'guide': guide
    }
    return render(request, 'guide.html', context)


def send_appraisal(request):
    form = Appraisal(request.POST or None)
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
                                                  'form': Appraisal()})

    return render(request, 'appraisal.html', {'form': Appraisal()})