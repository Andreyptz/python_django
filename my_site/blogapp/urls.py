from django.urls import path

from .views import BasedView, ArticleCreateView

app_name = "blogapp"

urlpatterns = [
    path('', BasedView.as_view(), name='articles'),
    path('create_article/', ArticleCreateView.as_view(), name='create_article'),
]