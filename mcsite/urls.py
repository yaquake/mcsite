from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf.urls.static import static, settings

urlpatterns = [
    path('jet/', include('jet.urls', namespace='jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', namespace='jet-dashboard')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('napoleon/', admin.site.urls, name='napoleon'),
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('properties/page<int:page>', views.properties, name='properties'),
    path('contact/', views.contact, name='contact'),
    path('apply/', views.apply, name='apply'),
    path('about/', views.about, name='about'),
    path('summernote/', include('django_summernote.urls')),
    path('postnews/', views.postnews, name='postnews'),
    path('news/page<int:page>', views.news, name='news'),
    path('news/<str:slug>', views.news_details, name='news_details'),
    # path('about/addperson', views.add_person, name='add_person'),
    path('properties/<str:key>', views.property_details, name='property_details'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
