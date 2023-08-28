from django.core.management import BaseCommand

from blogapp.models import Article, Author, Tag, Category

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create author")
        authors = [
            "Max",
            "Alex",
            "Ron"
        ]

        for author_name in authors:
            author, created = Author.objects.get_or_create(name=author_name)
            self.stdout.write(f'Created article {author.name}')

        self.stdout.write(self.style.SUCCESS("Author created"))

# КАТЕГОРИИ СТАТЕЙ
        self.stdout.write("Create category")
        categories = [
            "Study",
        ]

        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            self.stdout.write(f'Created category {category}')

        self.stdout.write(self.style.SUCCESS("Category created"))

# ТЭГИ
        tags = [
            "skillbox",
            "IT",
            "python"
        ]
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(f"Created tag {tag.name}")
        self.stdout.write(self.style.SUCCESS("Tag created"))
