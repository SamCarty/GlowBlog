from django.http import JsonResponse
from django.shortcuts import render, redirect

from comments.models import Comment


def list_all(request):
    queryset = Comment.objects.order_by('-created_date').values()
    return JsonResponse({'comments': list(queryset)})


def new(request, article_id):
    if request.method == 'POST':
        author = request.user
        content = request.POST['content']

        comment = Comment(author=author, content=content, article_id=article_id)
        comment.save()

        return redirect('list_all')
    else:
        return render(request, 'add_comment.html')


def delete(request, comment_id):
    if request.user.is_authenticated and request.user.is_superuser:
        article = Comment.objects.filter(id=comment_id)
        article.delete()

    return redirect('list_all')
