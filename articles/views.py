from django.http import JsonResponse
from django.shortcuts import redirect, render

from articles.models import Article


def list_all(request):
    queryset = Article.objects.order_by('-created_date').values()
    return JsonResponse({'articles': list(queryset)})


def new(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            author = request.user
            title = request.POST['title']
            content = request.POST['content']

            article = Article(author=author, title=title, content=content)
            article.save()

            return redirect('list_all')

    else:
        return render(request, 'add_article.html')


def delete(request, article_id):
    if request.user.is_authenticated and request.user.is_superuser:
        article = Article.objects.filter(id=article_id)
        article.delete()

    return redirect('list_all')
