from django.urls import path

from .views import (
    # BasedView,
    ArticleCreateView,
    ArticleListView,
    ArticleDetailView,
    LatestArticlesFeed,
)

app_name = "blogapp"

urlpatterns = [
    # path('', BasedView.as_view(), name='articles'),
    path('create_article/', ArticleCreateView.as_view(), name='create_article'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticlesFeed(), name='articles-feed'),
]