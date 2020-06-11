from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from articles.models import Article
from articles.serializers import ArticleSerializer

SAFE_METHODS = ('get', 'list', 'retrieve')


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.order_by('-created_date')
    serializer_class = ArticleSerializer

    def has_object_permission(self, request, view, obj):
        # allow all users (even non-logged in users) to get, list and retrieve articles
        if request.method in SAFE_METHODS:
            return True

        # for all other actions, the user must be admin
        return IsAdminUser

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
