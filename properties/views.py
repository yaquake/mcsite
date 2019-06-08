from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Property


# List of properties
class PropertyListView(ListView):
    template_name = 'listings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_count'] = Property.objects.all().count()
        return context

    def get_queryset(self):
        page_ = self.kwargs.get('page')
        property_ = Property.objects.all()
        paginator = Paginator(property_, 9)
        return paginator.page(page_)


# Property details of every properties
class PropertyDetailView(DetailView):
    template_name = 'property_details.html'

    def get_object(self, queryset=None):
        code_ = self.kwargs.get('key')
        return get_object_or_404(Property, code=code_)

