from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from articles.models import Article
from articles.serializers import ArticleSerializer

SAFE_METHODS = ('list', 'retrieve')


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.order_by('-created_date')
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
