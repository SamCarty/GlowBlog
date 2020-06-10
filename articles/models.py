from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
