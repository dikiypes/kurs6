from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_post_list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # Увеличиваем количество просмотров при каждом просмотре деталей статьи
        post = self.get_object()
        post.views += 1
        post.save()
        return super().get(request, *args, **kwargs)
