from django.db import models


class Message(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    content = models.CharField(null=False, max_length=255)
    #sender = models.ForeignKey('User', null=False, related_name='messages')
    state = models.CharField(null=False, default='sent', max_length=255)  # sent, delivered, viewed
