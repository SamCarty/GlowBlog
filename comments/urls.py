from django.urls import path

from comments import views

urlpatterns = [
    path('', views.list_all, name='list_all'),
    path('new/<int:article_id>', views.new, name='new'),
    path('delete/<int:comment_id>', views.delete, name='delete')
]
