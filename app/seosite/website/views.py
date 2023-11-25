from .models import Page
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse

import datetime, os


@require_GET
def robots_txt(request):
    robots_txt_content = f"""
    User-agent: *
    Disallow:

    Sitemap: {request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))}
    """
    return HttpResponse(robots_txt_content, content_type="text/plain")


class HomeView(TemplateView):
    template_name = f"common/{os.getenv('SITE_TEMPLATE')}/views/home.html"


# Create your views here.
class PageListView(ListView):
    queryset = Page.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
    template_name = f"common/{os.getenv('SITE_TEMPLATE')}/views/page/list.html"


class PageDetailView(DetailView):
    model = Page
    context_object_name = "page"
    template_name = f"common/{os.getenv('SITE_TEMPLATE')}/views/page/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
