from django.core.management import BaseCommand

from blogapp.models import Article

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create article")
        titles = [
            "My Training",
        ]

        for title in titles:
            article = Article.objects.get_or_create(title=title, author="Max")
            self.stdout.write(f'Created article {article.title}')

        self.stdout.write(self.style.SUCCESS("Article created"))
