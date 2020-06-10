from django.urls import path

from articles import views

urlpatterns = [
    path('', views.list_all, name='list_all'),
    path('new/', views.new, name='new'),
    path('delete/<int:article_id>', views.delete, name='delete')
]
