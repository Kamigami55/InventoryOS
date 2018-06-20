# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# from django.http import HttpResp
from django.shortcuts import render_to_response



def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render_to_response('index.html')
