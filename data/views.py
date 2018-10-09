# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import JsonResponse

from models import Reference

# Create your views here.

def showTable(request):
    references = Reference.objects.all()
    return render(request, 'data/data.html',
     context={'references': references})

def deleteData(request):
    Reference.objects.all().delete()
    return JsonResponse('', safe=False)
