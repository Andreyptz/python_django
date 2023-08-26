from typing import Sequence

from django.core.management import BaseCommand

from blogapp.models import Article, Author, Tag, Category
from django.db import transaction


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write("Create article with author")
        author = Author.objects.get(name="Ron")
        tags: Sequence[Tag] = Tag.objects.all()
        article, created = Article.objects.defer('content').get_or_create(
            title="My training",
        )
        for tag in tags:
            article.tags.add(tag)
        article.save()

        self.stdout.write(self.style.SUCCESS(f"Article '{article.title}' created"))
