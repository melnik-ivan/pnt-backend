from rest_framework import serializers
from messenger import models
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    room = serializers.ReadOnlyField(source='room.title')

    class Meta:
        model = models.Message
        fields = (
            'id', 'content', 'owner', 'room',
        )


class RoomSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = models.Room
        fields = (
            'id', 'title', 'owner', 'members', 'messages',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'rooms', 'messages')

