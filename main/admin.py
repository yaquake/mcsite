from django.contrib import admin
from .models import News, Person, Property, Palace, Services, MainPageInfo
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class MainPageInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


admin.site.register(News, NewsAdmin)

admin.site.register(Person)

admin.site.register(Property)

admin.site.register(Palace)

admin.site.register(Services)

admin.site.register(MainPageInfo, MainPageInfoAdmin)