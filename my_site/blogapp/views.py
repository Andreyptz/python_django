from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from blogapp.models import Author, Article


class BasedView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    queryset = (Author.objects.all())

class ArticleCreateView(CreateView):
    template_name = 'blogapp/create_article.html'
    model = Article
    fields = "title", "author", "content", "tags"
    success_url = reverse_lazy("blogapp:articles")

