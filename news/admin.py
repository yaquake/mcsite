from django.contrib import admin
from .models import News
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


admin.site.register(News, NewsAdmin)