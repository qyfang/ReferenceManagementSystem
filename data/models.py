# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Reference(models.Model):
    selfid = models.CharField(max_length=30, unique=True)

    url = models.URLField(unique=True)

    title = models.CharField(max_length=200)

    authors = models.TextField(blank=True)

    keywords = models.TextField(blank=True)

    abstract = models.TextField(blank=True)

    referids = models.TextField(blank=True)