from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from articles.models import Article
from comments.models import Comment


def list_all(request):
    queryset = Comment.objects.order_by('-created_date').values()
    return JsonResponse({'comments': list(queryset)})


def new(request, article_id):
    article = Article.objects.filter(id=article_id)
    if article.count() == 0:
        return HttpResponseNotFound('Article does not exist')

    if request.method == 'POST':
        author = request.user
        content = request.POST['content']

        comment = Comment(author=author, content=content, article_id=article_id)
        comment.save()

        return redirect('comments:list_all')
    else:
        return render(request, 'add_comment.html')


def delete(request, comment_id):
    if request.user.is_authenticated and request.user.is_superuser:
        article = Comment.objects.filter(id=comment_id)
        article.delete()
        return redirect('comments:list_all')

    else:
        return HttpResponse('Unauthorised', status=401)
