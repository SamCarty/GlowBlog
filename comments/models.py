from django.db import models

from articles.models import Article


class Comment(models.Model):
    username = models.CharField(max_length=50, null=True)
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]
