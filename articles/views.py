from datetime import datetime

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404

from articles.models import Article


def list_all(request):
    queryset = Article.objects.order_by('-created_date').values()
    return JsonResponse({'articles': list(queryset)})


def new(request):
    """
    Allows a superuser to create a brand new article.
    :return: If the user is not authenticated, we return 401 unauthorised error.
        If the request is a GET request, we return the template to edit the article!
        If the article has been added, redirect to the articles list.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            author = request.user
            title = request.POST['title']
            content = request.POST['content']

            article = Article(author=author, title=title, content=content)
            article.save()

            return redirect('articles:list_all')
        else:
            return render(request, 'add_article.html')
    else:
        return HttpResponse('Unauthorised', status=401)


def delete(request, article_id):
    """
    Allows a superuser to delete an existing article by its id.
    :return: If the user is not authenticated, we return 401 unauthorised error.
        If the article has been deleted, redirect to the articles list.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        article = Article.objects.filter(id=article_id)
        if article.count() == 0:
            return HttpResponseNotFound('Article does not exist')

        article.delete()
        return redirect('articles:list_all')
    else:
        return HttpResponse('Unauthorised', status=401)


def edit(request, article_id):
    """
    Allows a superuser to edit an existing article by its id.
    :return: If the article does not exist, we return a 404 error.
        If the user is not authenticated, we return 401 unauthorised error.
        If the request is a GET request, we return the template to edit the article!
        If the article has been edited, redirect to the articles list.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        article = get_object_or_404(Article, id=article_id)
        if request.method == 'POST':
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.last_modified_date = datetime.now()
            article.save()
            return redirect('articles:list_all')
        else:
            return render(request, 'edit_article.html')
    else:
        return HttpResponse('Unauthorised', status=401)


def view(request, article_id):
    articles = Article.objects.filter(id=article_id)
    if articles.count() == 0:
        return HttpResponseNotFound("Article does not exist")

    return JsonResponse({'article': list(articles.values())})
