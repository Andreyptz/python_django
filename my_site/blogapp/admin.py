from django.contrib import admin

from .models import Author, Article

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_display = "id", "title", "pub_date", "author"
    list_display_links = "id", "title"
