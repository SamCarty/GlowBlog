from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ('title', 'content', 'author')
