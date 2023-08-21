from django.core.management import BaseCommand

from blogapp.models import Article, Author, Tag

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
            print(created)

        self.stdout.write(self.style.SUCCESS("Author created"))

        tags = [
            "skillbox",
            "it",
            "python"
        ]
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            print(created)
            self.stdout.write(f"Created tag {tag.name}")
        self.stdout.write(self.style.SUCCESS("Tag created"))
