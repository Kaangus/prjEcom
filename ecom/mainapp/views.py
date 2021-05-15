from django.shortcuts import render
from django.views.generic import DetailView
from .models import *

def base(request):
    return render(request, 'base.html', {})

class ProductPageView(DetailView):

    CT_MODEL_CLASS = {
        'susi': Susi,
        'pizza': Pizza
    }

    def dispatch(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_page.html'
    slug_url_kwarg = 'slug'
