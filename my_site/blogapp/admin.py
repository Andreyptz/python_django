from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_display = "id", "title", "content", "pub_date", "author"
    list_display_links = "id", "title"
