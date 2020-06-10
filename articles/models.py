from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(default=datetime.now)
    last_modified_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
