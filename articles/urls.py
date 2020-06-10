from django.urls import path, include
from rest_framework import routers

from articles import views

router = routers.DefaultRouter()
router.register(r'', views.ArticleViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
