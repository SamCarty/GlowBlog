from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from articles.models import Article
from comments.models import Comment
from comments.views import CommentViewSet


class CommentTestCase(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(username='admin')
        self.normal_user = get_user_model().objects.create(username='normal')
        self.article = Article.objects.create(title='test article', content='this is some content')

        self.valid_data = {
            'content': 'this is a comment',
            'article': 1
        }
        self.valid_optional_data = {
            'content': 'this is a comment',
            'article': 1,
            'username': 'test'
        }
        self.invalid_data = {
            'content': 'this is a comment',
            'article': 2
        }

    @staticmethod
    def setup_list_request(user):
        factory = APIRequestFactory()
        request = factory.get('/comments/', format='json')
        force_authenticate(request, user)
        view = CommentViewSet.as_view({'get': 'list'})
        return view(request=request)
    
    def comment_list(self, user):
        """ Checks that the given user can request a list of all the comments.
         @:param user the Django User object that should make the request. """
    
        # ensure the response is OK when there is no data
        response = self.setup_list_request(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0, 'Response was not of size 0, despite no comments added.')
    
        # create a test comment and ensure its in the database
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()
        self.assertEqual(Comment.objects.get().content, comment.content)
        self.assertEqual(Comment.objects.get().article, comment.article)

        # check if the comment in the database can be retrieved
        response = self.setup_list_request(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, 'Response was not of size 1, despite an article in database.')
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['content'], comment.content)
        self.assertEqual(response.data[0]['article'], comment.article_id)

    def test_list_admin(self):
        self.comment_list(self.admin_user)

    def test_list_non_admin(self):
        self.comment_list(self.normal_user)

    @staticmethod
    def setup_create_request(user, data):
        factory = APIRequestFactory()
        request = factory.post('/comments/', data,
                               format='json')

        if user is not None:
            force_authenticate(request, user)

        view = CommentViewSet.as_view({'post': 'create'})
        return view(request=request)

    def test_create_with_valid_data(self):
        """ Checks that a POST request is successful if the authenticated user is an admin. """
        response = self.setup_create_request(self.admin_user, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_data['content'])
        self.assertEqual(Comment.objects.get().username, self.admin_user.username)
        self.assertEqual(Comment.objects.get().article, self.article)

    def test_create_with_valid_data_non_admin(self):
        """ Checks that a POST request is successful if the authenticated user is not an admin. """
        response = self.setup_create_request(self.normal_user, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_data['content'])
        self.assertEqual(Comment.objects.get().username, self.normal_user.username)
        self.assertEqual(Comment.objects.get().article, self.article)

    def test_create_with_valid_data_non_authenticated(self):
        """ Checks that a POST request is successful if the authenticated user is not authenticated. """
        response = self.setup_create_request(None, self.valid_optional_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_optional_data['content'])
        self.assertEqual(Comment.objects.get().username, self.valid_optional_data['username'])
        self.assertEqual(Comment.objects.get().article, self.article)

    def test_create_with_invalid_data(self):
        """ Checks that a POST request is rejected if some invalid data is supplied. """
        response = self.setup_create_request(self.admin_user, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    @staticmethod
    def setup_retrieve_request(user, comment):
        factory = APIRequestFactory()
        request = factory.get('/comments/', format='json')

        force_authenticate(request, user)
        view = CommentViewSet.as_view({'get': 'retrieve'})
        return view(request=request, pk=comment.pk)

    def test_retrieve_admin(self):
        """ Check that a GET request is successful if the authenticated user is an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()
        response = self.setup_retrieve_request(self.admin_user, comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['content'], comment.content)
        self.assertEqual(response.data['article'], self.article.id)

    def test_retrieve_non_admin(self):
        """ Check that a GET request is rejected if the authenticated user is not an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()
        response = self.setup_retrieve_request(self.normal_user, comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['content'], comment.content)
        self.assertEqual(response.data['article'], self.article.id)

    @staticmethod
    def setup_update_request(user, comment, data):
        factory = APIRequestFactory()
        request = factory.put('/comments/' + str(comment.pk) + '/', data, format='json')

        force_authenticate(request, user)
        view = CommentViewSet.as_view({'put': 'update'})
        return view(request=request, pk=comment.pk)

    def test_update_valid_data_admin(self):
        """ Check that a PUT request is successful if the authenticated user is an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()

        data = {
            'content': 'changed',
            'article': 1
        }

        response = self.setup_update_request(self.admin_user, comment, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, data['content'])
        self.assertEqual(Comment.objects.get().article, self.article)

    def test_update_invalid_data_admin(self):
        """ Check that a PUT request is rejected if the authenticated user is not an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()

        response = self.setup_update_request(self.admin_user, comment, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_data['content'])
        self.assertEqual(Comment.objects.get().article, self.article)

    @staticmethod
    def setup_delete_request(user, comment):
        factory = APIRequestFactory()
        request = factory.delete('/comments/' + str(comment.pk) + '/', format='json')

        force_authenticate(request, user)
        view = CommentViewSet.as_view({'delete': 'destroy'})
        return view(request=request, pk=comment.pk)

    def test_delete_admin(self):
        """ Check that a DELETE request is successful if the authenticated user is an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_data['content'])
        self.assertEqual(Comment.objects.get().article, self.article)

        response = self.setup_delete_request(self.admin_user, comment)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_non_admin(self):
        """ Check that a DELETE request is rejected if the authenticated user is not an admin. """
        comment = Comment.objects.create(content=self.valid_data['content'], article_id=self.valid_data['article'])
        comment.save()

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, self.valid_data['content'])
        self.assertEqual(Comment.objects.get().article, self.article)
    
        response = self.setup_delete_request(self.normal_user, comment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)
