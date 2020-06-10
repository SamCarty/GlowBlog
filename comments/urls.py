from django.urls import path

from comments import views

app_name = 'comments'
urlpatterns = [
    path('', views.list_all, name='list_all'),
    path('<int:article_id>/new', views.new, name='new'),
    path('<int:comment_id>/delete', views.delete, name='delete')
]
