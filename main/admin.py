from django.contrib import admin
from .models import News, Person
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


admin.site.register(News, NewsAdmin)

admin.site.register(Person)