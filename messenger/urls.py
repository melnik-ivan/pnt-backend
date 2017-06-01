from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from messenger import views

router = DefaultRouter()
router.register(r'messages', views.MessageViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
