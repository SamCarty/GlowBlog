from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from articles.models import Article


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(default=datetime.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]
