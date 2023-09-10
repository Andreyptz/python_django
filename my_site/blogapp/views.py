from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView

from blogapp.models import Article, Author

class ArticleListView(ListView):
    queryset = (
        Article.objects
        .filter(pub_date__isnull=False)
        .order_by("-pub_date")
    )

class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Update on changes and addintion blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (
            Article.objects
            .filter(pub_date__isnull=False)
            .order_by("-pub_date")[:5]
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:300]
    #
    # def item_link(self, item: Article):
    #     return reverse("blogapp:article", kwargs={"pk": item.pk})

# class BasedView(ListView):
#     template_name = 'blogapp/article_list.html'
#     context_object_name = 'articles'
#     queryset = (Article.objects
#                 .defer('content')
#                 .select_related("author", "category")
#                 .prefetch_related("tags")
#                 )

class ArticleCreateView(LoginRequiredMixin, CreateView):

    template_name = 'blogapp/create_article.html'
    model = Article
    fields = "title", "author", "content", "category", "tags"
    success_url = reverse_lazy("blogapp:articles")
