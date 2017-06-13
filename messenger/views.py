from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
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
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class MessageList(APIView):

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

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = serializers.MessageSerializerReadOnlyRoom
        return serializer_class


class RoomList(APIView):

    def get(self, request, format=None):
        rooms = request.user.rooms.all()
        serializer = serializers.RoomSerializer(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = serializers.RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [RoomPermissions]


class CurrentUser(APIView):

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = serializers.UserSerializer(user)
        return JsonResponse(serializer.data)