from django.urls import path, include
from rest_framework import routers

from comments import views

router = routers.DefaultRouter()
router.register(r'', views.CommentViewset)

urlpatterns = [
    path('', include(router.urls)),
]
