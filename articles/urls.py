from django.urls import path

from articles import views

app_name = 'articles'
urlpatterns = [
    path('', views.list_all, name='list_all'),
    path('new', views.new, name='new'),
    path('<int:article_id>/delete', views.delete, name='delete'),
    path('<int:article_id>/edit', views.edit, name='edit'),
    path('<int:article_id>', views.view, name='view')
]
