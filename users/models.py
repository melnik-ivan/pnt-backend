from django.db import models


class User(models.Model):
    created = models.DateTimeField(null=False, auto_now_add=True)
    email = models.EmailField(null=False)

