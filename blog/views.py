# Create your views here.
from django.shortcuts import render

from django.views.generic.base import TemplateView


class HomeView(TemplateView):

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['content'] = "Hello world"
        return context
