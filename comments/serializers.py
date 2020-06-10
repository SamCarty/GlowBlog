from rest_framework import serializers

from comments.models import Comment
from articles.models import Article


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.PrimaryKeyRelatedField(many=False, queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ('article', 'username', 'content')
