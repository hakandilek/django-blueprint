from django.http import HttpResponse
from django.contrib.auth.models import User
from minimar.utils import json_encode

def user_json(request, name=None):
    if name:
        q = User.objects.filter(name__istartswith=name).order_by('username')
    else:
        q = User.objects.all().order_by('username')
    
    data = json_encode(q, only=['username'])
    return HttpResponse(data, mimetype="text/plain")
