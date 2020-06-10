from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Article


class ArticleEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="wonderwoman", password="password")
        self.superuser = User.objects.create_superuser(username='superman', password="password")

    def test_new_article_form(self):
        self.client.force_login(self.superuser)

        url = reverse('articles:new')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'add_article.html',
                                'GET request for new article did not return the correct form.')

    def test_superuser_can_add_article(self):
        self.client.force_login(self.superuser)

        data = {'title': 'my article',
                'content': 'some really enthralling blog post here...'}

        self.client.post(reverse('articles:new'), data)

        exists = Article.objects.all().count() > 0
        self.assertTrue(exists, 'Superuser could not add a new article')

    def test_new_article_in_database(self):
        self.client.force_login(self.superuser)

        data = {'title': 'my article',
                'content': 'some really enthralling blog post here...'}

        self.client.post(reverse('articles:new'), data)

        article = Article.objects.get()

        self.assertEqual(article.title, 'my article')
        self.assertEqual(article.content, 'some really enthralling blog post here...')
        self.assertEqual(article.author, self.superuser)

    def test_regular_user_cannot_add_article(self):
        self.client.force_login(self.user)

        data = {'title': 'my article',
                'content': 'some really enthralling blog post here...'}

        response = self.client.post(reverse('articles:new'), data)
        self.assertEqual(response.status_code, 401, 'User did not receive a "401 unauthorised" response code')

        exists = Article.objects.all().count() > 0
        self.assertFalse(exists, 'User was able to add a new article')

    def test_list_all_articles(self):
        self.client.force_login(self.superuser)

        data = {'title': 'my article',
                'content': 'some really enthralling blog post here...'}

        self.client.post(reverse('articles:new'), data)

        data2 = {'title': 'my second article',
                'content': 'some really enthralling blog post here...'}
        self.client.post(reverse('articles:new'), data2)

        # check both the articles were added to the database
        exists = Article.objects.all().count() == 2
        self.assertTrue(exists, 'One or both articles were not returned')

        # check response code is OK
        response = self.client.get(reverse('articles:list_all'))
        self.assertEqual(response.status_code, 200, 'Bad status code returned')

        # checks that the articles are returned in reverse-chronological order
        self.assertEqual(response.json()['articles'][0]['title'], 'my second article')
        self.assertEqual(response.json()['articles'][1]['title'], 'my article')
