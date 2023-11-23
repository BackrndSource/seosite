from .models import Category, Post, Image, Comment, Config
from django.views.generic import ListView, DetailView
import datetime

import os

# from rest_framework.parsers import MultiPartParser, FormParser


class HomeView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostListView(ListView):
    queryset = (
        Post.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now()).order_by("-last_modified")
    )
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/post/list.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/post/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())


class CategoryListView(ListView):
    queryset = Category.objects.filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/category/list.html"


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/category/detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible=True).exclude(publish_date__gte=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ALL POSTS
        posts = (
            self.get_object()
            .posts.filter(visible=True)
            .exclude(publish_date__gte=datetime.datetime.now())
            .order_by("-last_modified")
        )
        context["featured_posts"] = posts.filter(featured=True)
        return context
