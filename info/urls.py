from django.urls import path
from .models import *
from .views import (
    why_us,
    send_appraisal,
    tenancy,
    ContactView,
    ApplyView,
    AboutView,
    ServicesListView
)

app_name = 'info'
urlpatterns = [
    path('whyus/', why_us, name='whyus'),
    path('appraisal/', send_appraisal, name='appraisal'),
    path('tenancy_guide/', tenancy, name='tenancy'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('apply/', ApplyView.as_view(), name='apply'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesListView.as_view(), name='services'),

]
