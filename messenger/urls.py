from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from messenger import views

router = DefaultRouter()
# router.register(r'messages', views.MessageViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'messages/$', views.MessageList.as_view(), name='messages-list'),
    url(r'messages/(?P<pk>[0-9]+)/$', views.MessageDetailViewSet.as_view(), name='messages-detail'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
