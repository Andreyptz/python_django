from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True, db_index=True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=40, db_index=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=20, db_index=True)
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=True, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="articles")

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk": self.pk})