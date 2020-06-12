from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from comments.models import Comment
from comments.serializers import CommentSerializer

SAFE_METHODS = ('list', 'retrieve', 'create')


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('article_id')
    serializer_class = CommentSerializer

    def has_object_permission(self, request, view, obj):
        # allow all users (even non-logged in users) to get, list, retrieve and create comments
        if request.method in SAFE_METHODS:
            return True

        # for all other actions, the user must be admin
        return IsAdminUser

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save(username=self.request.user.username)
        else:
            serializer.save(username=self.request.POST['username'])
