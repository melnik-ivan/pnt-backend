from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework import viewsets, generics, status

from messenger import serializers
from messenger import models
from messenger.permissions import RoomPermissions, MessagePermissions


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer



class MessageList(APIView):
    renderer_classes = [BrowsableAPIRenderer]
    def get(self, request, format=None):
        messages = models.Message.objects.filter(room__in=request.user.rooms.all())
        serializer = serializers.MessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = serializers.MessageSerializer(data=data)
        if serializer.is_valid():
            if serializer.validated_data['room'] in request.user.rooms.all():
                serializer.save(owner=request.user)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    # if owner -> RUD IsOwner
    # if in message room members -> CR IsInMessageRoomMembers
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [MessagePermissions]


class RoomViewSet(viewsets.ModelViewSet):
    # if owner -> RUD IsOwner
    # if room member -> R IsRoomMember
    # if other -> C IsAuthenticated
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (RoomPermissions,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
