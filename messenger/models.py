from django.db import models


class Message(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False)


class Room(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='created_rooms', on_delete=models.CASCADE)
    members = models.ManyToManyField('auth.User', related_name='rooms')
    title = models.CharField(max_length=255, null=False)
