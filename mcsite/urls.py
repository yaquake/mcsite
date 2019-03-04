from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf.urls.static import static, settings
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap, PropertySitemap, NewsSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'property': PropertySitemap,
    'news': NewsSitemap,

}

urlpatterns = [
    path('jet/', include('jet.urls', namespace='jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('napoleon/', admin.site.urls, name='admin'),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('listings/page<int:page>', views.listings, name='listings'),
    path('contact/', views.contact, name='contact'),
    path('apply/', views.apply, name='apply'),
    path('about/', views.about, name='about'),
    path('summernote/', include('django_summernote.urls')),
    path('postnews/', views.postnews, name='postnews'),
    path('news/page<int:page>', views.news, name='news'),
    path('news/<str:slug>', views.news_details, name='news_details'),
    path('listings/<str:key>', views.property_details, name='property_details'),
    path('appraisal/', views.send_appraisal, name='appraisal'),
    path('tenancy_guide/', views.tenancy, name='tenancy'),
    path('whyus/', views.whyus, name='whyus'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    from .local_urls import *
except ImportError:
    pass
