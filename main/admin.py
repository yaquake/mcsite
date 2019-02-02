from django.contrib import admin
from .models import News, Person, Property, Palace, Services, MainPageInfo, About
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class MainPageInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(About, AboutAdmin)

admin.site.register(News, NewsAdmin)

admin.site.register(Person)

admin.site.register(Property)

admin.site.register(Palace)

admin.site.register(Services)

admin.site.register(MainPageInfo, MainPageInfoAdmin)