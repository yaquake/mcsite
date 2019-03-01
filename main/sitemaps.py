from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Property, News


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home', 'apply', 'services', 'contact', 'about']

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):

    def items(self):
        return Property.objects.all()


class NewsSitemap(Sitemap):

    def items(self):
        return News.objects.all()