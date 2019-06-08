from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf.urls.static import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .views import PropertyDetailView, PropertyListView


app_name = 'properties'
urlpatterns = [
    path('page<int:page>/',
         cache_page(getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT))(PropertyListView.as_view()), name='listings'),
    path('<str:key>/',
         cache_page(getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT))(PropertyDetailView.as_view()),
         name='property_details'),
]
