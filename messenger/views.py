from rest_framework import viewsets, permissions

from django.contrib.auth.models import User

from messenger import serializers
from messenger import models
from messenger.permissions import RoomPermissions, MessagePermissions


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    # if owner -> RUD IsOwner
    # if in message room members -> CR IsInMessageRoomMembers
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (MessagePermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    # if owner -> RUD IsOwner
    # if room member -> R IsRoomMember
    # if other -> C IsAuthenticated
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (RoomPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
