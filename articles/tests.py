from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from articles.models import Article
from articles.views import ArticleViewset


class ArticleTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin')
        self.normal_user = User.objects.create(username='normal')
        self.valid_data = {
            'title': 'test article',
            'content': 'this is some content'
        }
        self.invalid_data = {
            'title': '',
            'content': 'this is some content'
        }

    @staticmethod
    def setup_list_request(user):
        factory = APIRequestFactory()
        request = factory.get('/articles/', format='json')
        force_authenticate(request, user)
        view = ArticleViewset.as_view({'get': 'list'})
        return view(request=request)

    def article_list(self, user):
        """ Checks that the given user can request a list of all the articles.
         @:param user the Django User object that should make the request. """

        # ensure the response is OK when there is no data
        response = self.setup_list_request(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0, 'Response was not of size 0, despite no articles added.')

        # create a test article and ensure its in the database
        article = Article.objects.create(title='test article', content='this is some content')
        article.save()
        self.assertEqual(Article.objects.get().title, article.title)
        self.assertEqual(Article.objects.get().content, article.content)

        # check if the article in the database can be retrieved
        response = self.setup_list_request(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, 'Response was not of size 1, despite an article in database.')
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['title'], article.title)
        self.assertEqual(response.data[0]['content'], article.content)

    def test_list_admin(self):
        self.article_list(self.admin_user)

    def test_list_non_admin(self):
        self.article_list(self.normal_user)

    @staticmethod
    def setup_create_request(user, data):
        factory = APIRequestFactory()
        request = factory.post('/articles/', data,
                               format='json')

        force_authenticate(request, user)
        view = ArticleViewset.as_view({'post': 'create'})
        return view(request=request)

    def test_create_with_valid_data(self):
        """ Checks that a POST request is successful if the authenticated user is an admin. """
        response = self.setup_create_request(self.admin_user, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, self.valid_data['title'])
        self.assertEqual(Article.objects.get().content, self.valid_data['content'])

    def test_create_with_invalid_data(self):
        """ Checks that a POST request is rejected if some invalid data is supplied. """
        response = self.setup_create_request(self.admin_user, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Article.objects.count(), 0)

    def test_create_non_admin(self):
        """ Checks that a POST request is rejected if the authenticated user is not an admin. """
        response = self.setup_create_request(self.normal_user, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 0)

    @staticmethod
    def setup_retrieve_request(user, article):
        factory = APIRequestFactory()
        request = factory.get('/articles/', format='json')

        force_authenticate(request, user)
        view = ArticleViewset.as_view({'get': 'retrieve'})
        return view(request=request, pk=article.pk)

    def test_retrieve_admin(self):
        """ Check that a GET request is successful if the authenticated user is an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()
        response = self.setup_retrieve_request(self.admin_user, article)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], article.title)
        self.assertEqual(response.data['content'], article.content)

    def test_retrieve_non_admin(self):
        """ Check that a GET request is rejected if the authenticated user is not an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()
        response = self.setup_retrieve_request(self.normal_user, article)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], article.title)
        self.assertEqual(response.data['content'], article.content)

    @staticmethod
    def setup_update_request(user, article, data):
        factory = APIRequestFactory()
        request = factory.put('/articles/' + str(article.pk) + '/', data, format='json')

        force_authenticate(request, user)
        view = ArticleViewset.as_view({'put': 'update'})
        return view(request=request, pk=article.pk)

    def test_update_valid_data_admin(self):
        """ Check that a PUT request is successful if the authenticated user is an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()

        data = {
            'title': 'changed',
            'content': 'also changed'
        }

        response = self.setup_update_request(self.admin_user, article, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, data['title'])
        self.assertEqual(Article.objects.get().content, data['content'])

    def test_update_invalid_data_admin(self):
        """ Check that a PUT request is rejected if the authenticated user is not an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()

        response = self.setup_update_request(self.admin_user, article, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, self.valid_data['title'])
        self.assertEqual(Article.objects.get().content, self.valid_data['content'])

    @staticmethod
    def setup_delete_request(user, article):
        factory = APIRequestFactory()
        request = factory.delete('/articles/' + str(article.pk) + '/', format='json')

        force_authenticate(request, user)
        view = ArticleViewset.as_view({'delete': 'destroy'})
        return view(request=request, pk=article.pk)

    def test_delete_admin(self):
        """ Check that a DELETE request is successful if the authenticated user is an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, self.valid_data['title'])
        self.assertEqual(Article.objects.get().content, self.valid_data['content'])

        response = self.setup_delete_request(self.admin_user, article)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_delete_non_admin(self):
        """ Check that a DELETE request is rejected if the authenticated user is not an admin. """
        article = Article.objects.create(title=self.valid_data['title'], content=self.valid_data['content'])
        article.save()

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, self.valid_data['title'])
        self.assertEqual(Article.objects.get().content, self.valid_data['content'])

        response = self.setup_delete_request(self.normal_user, article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 1)
