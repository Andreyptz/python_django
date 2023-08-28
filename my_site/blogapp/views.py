from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blogapp.models import Article, Author


class BasedView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    queryset = (Article.objects
                .defer('content')
                .select_related("author")
                .prefetch_related("tags")
                )

class ArticleCreateView(LoginRequiredMixin, CreateView):

    template_name = 'blogapp/create_article.html'
    model = Article
    fields = "title", "author", "content", "category", "tags"
    success_url = reverse_lazy("blogapp:articles")
