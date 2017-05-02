# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    date = models.DateField(auto_now=True)
    anonymous = models.BooleanField()
    sender = models.ForeignKey(User, related_name="sender")
    recipient = models.ForeignKey(User, related_name="recipient")
    text = models.TextField()
    hint = models.TextField()