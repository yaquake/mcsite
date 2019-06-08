from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class MainPageInfoAdmin(SummernoteModelAdmin):
    summernote_fields = ['description', ]


class AboutAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


class ContactAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


class WhyUsAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


class GuideAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register(EmailSettings)

admin.site.register(ContactUs, ContactAdmin)

admin.site.register(MottoEmailPhone)

admin.site.register(About, AboutAdmin)

admin.site.register(Person)

admin.site.register(Services)

admin.site.register(MainPageInfo, MainPageInfoAdmin)

admin.site.register(WhyUs, WhyUsAdmin)

admin.site.register(Guide, GuideAdmin)
