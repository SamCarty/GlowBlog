from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer

SAFE_METHODS = ('list', 'retrieve', 'create')


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('article_id')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if request.user.is_authenticated:
            serializer.validated_data['username'] = request.user.username
        else:
            if 'username' in self.request.data:
                serializer.validated_data['username'] = request.data['username']
            else:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
