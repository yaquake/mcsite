from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from django.contrib.sitemaps.views import sitemap
from info.sitemaps import StaticViewSitemap, PropertySitemap, NewsSitemap
from info.views import (
    Home,
    LogoutView,
    LoginView,
)

sitemaps = {
    'static': StaticViewSitemap,
    'properties': PropertySitemap,
    'news': NewsSitemap,

}

urlpatterns = [
    path('jet/', include('jet.urls', namespace='jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('python/', admin.site.urls, name='admin'),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', Home.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('news/', include('news.urls')),
    path('properties/', include('properties.urls')),
    path('info/', include('info.urls')),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    from .local_urls import *
except ImportError:
    pass
