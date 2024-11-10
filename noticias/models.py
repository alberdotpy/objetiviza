# En models.py
from django.db import models

class Periodico(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    alignment = models.CharField(max_length=50)
    replace_words = models.CharField(max_length=200)
    logo_url = models.URLField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Periodico, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    topic = models.CharField(max_length=200, null=True, blank=True)
    section = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    image_url = models.URLField(null=True, blank=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

