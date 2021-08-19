import uuid

from django.db import models
from django.urls import reverse


class Helpers:
    @staticmethod
    def delimiter(length: int = 8):
        return str(uuid.uuid4()).replace('-', '')[:length]


class Link(models.Model):
    id = models.CharField(max_length=32, default=Helpers.delimiter, primary_key=True, editable=False)
    original = models.URLField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.id} ➡️ {self.original}'


class Client(models.Model):
    address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    links = models.ManyToManyField(Link)
