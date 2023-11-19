from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.views.generic import TemplateView


@require_GET
def robots_txt(request):
    robots_txt_content = f"""
    User-agent: *
    Disallow:

    Sitemap: {request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))}
    """
    return HttpResponse(robots_txt_content, content_type="text/plain")


class HomeView(TemplateView):
    template_name = f"common/common/views/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
