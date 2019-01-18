from django.contrib import admin
from .models import News, Person, Property, Palace
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


admin.site.register(News, NewsAdmin)

admin.site.register(Person)

admin.site.register(Property)

admin.site.register(Palace)