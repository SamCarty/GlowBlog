from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from comments.models import Comment
from comments.serializers import CommentSerializer

SAFE_METHODS = ('get', 'list', 'retrieve', 'create')


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('article_id')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(self.__class__, self).get_permissions()

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save(username=self.request.user.username)
        else:
            serializer.save(username=self.request.POST['username'])
