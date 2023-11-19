from .models import Category, Post, Image, Comment, Config
from django.views.generic import ListView, DetailView
from django.utils import timezone

import os

# from rest_framework.parsers import MultiPartParser, FormParser


class HomeView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True)
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostListView(ListView):
    model = Post
    queryset = Post.objects.filter(visible=True).exclude(publish_date__gte=timezone.now())
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/post/list.html"


class PostDetailView(DetailView):
    context_object_name = "post"
    queryset = Post.objects.filter(visible=True).exclude(publish_date__gte=timezone.now())
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/post/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True)
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/category/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryDetailView(DetailView):
    context_object_name = "category"
    queryset = Category.objects.all()
    template_name = f"blog/{os.getenv('BLOG_TEMPLATE')}/views/category/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ALL POSTS
        posts = self.get_object().posts.filter(visible=True).exclude(publish_date__gte=timezone.now())
        context["featured_posts"] = posts.filter(featured=True).order_by("-last_modified")
        return context
