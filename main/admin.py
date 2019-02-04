from django.contrib import admin
from .models import News, Person, Property, Palace, Services, MainPageInfo, About, MottoEmailPhone, Contact
from django_summernote.admin import SummernoteModelAdmin


class NewsAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class MainPageInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


class ContactAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(Contact, ContactAdmin)

admin.site.register(MottoEmailPhone)

admin.site.register(About, AboutAdmin)

admin.site.register(News, NewsAdmin)

admin.site.register(Person)

admin.site.register(Property)

admin.site.register(Palace)

admin.site.register(Services)

admin.site.register(MainPageInfo, MainPageInfoAdmin)