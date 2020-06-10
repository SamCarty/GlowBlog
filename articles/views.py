from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from articles.models import Article
from articles.serializers import ArticleSerializer
from blog_rest.permissions import IsAdminUser

SAFE_METHODS = ('get', 'list', 'retrieve')


class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.order_by('-created_date')
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
