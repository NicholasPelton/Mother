#blog/views.py
from django.shortcuts import render
from garden.models import Garden, Outlet
from django.http import HttpResponse
from .models import Picture
from users.models import CustomUser
from django.conf import settings
import datetime
from django.utils.safestring import mark_safe
import json

def blog(request, username=None, garden=None):
    if request.method == "POST":
        print("GOT THE POST!")
        user = request.user.username
        garden = request.user.garden_set.get(name=garden)
        today = datetime.datetime.now().date()
        texts = request.POST['texts']
        pic = Picture.objects.get(photo='users/'+garden.serial+'/current.png')
        pic.comments = texts + '\r\n' + pic.comments
        pic.save()
        print ("Here is what it said:", pic.comments)
        return HttpResponse('')
        
    if username == request.user.username:
        garden = request.user.garden_set.get(name=garden)
        time_str = str(datetime.datetime.now())
        context = {'garden':garden, 'MEDIA_URL':settings.MEDIA_URL, 'time_now': datetime.datetime.now(), 'time_str':time_str,'room_name_json': mark_safe(json.dumps(garden.serial))}
        return render(request,'blog/blog.html',context)
    else: 
        return render(request,'users/no_access.html')
    

# Create your views here.
