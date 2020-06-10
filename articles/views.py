from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from articles.models import Article


def list_all(request):
    queryset = Article.objects.order_by('-created_date').values()
    return JsonResponse({'articles': list(queryset)})


def new(request):
    print("here")
    print(request.user)
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            print("authed")
            author = request.user
            title = request.POST['title']
            content = request.POST['content']

            article = Article(author=author, title=title, content=content)
            article.save()

            return redirect('list_all')

    else:
        return render(request, 'add_article.html')
