# garden/views.py
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CreateGardenForm
from .models import Garden, Outlet
from blog.models import Picture
from users.models import CustomUser
from django.http import HttpResponse
from . import consumers
import datetime
from django.utils.safestring import mark_safe
from django.conf import settings

# Create your views here.

''' CODE FOR UPDATING DON'T ACTIVATE ON ACCIDENT!
def update_mode_for_real(request, username=None, garden=None):
    print("trying to update")
    consumers.update_mode_for_real()
    return HttpResponse("Updating!")
'''

def gardens(request, username=None):
    media_cheat = settings.MEDIA_URL+ "users/"
    context={'media_cheat':media_cheat}
    if username == request.user.username:
        return render(request,'garden/gardens.html', context)
    else: 
        return render(request,'users/no_access.html')
        
def garden(request, username=None, garden=None):
    if request.method == 'POST':
        for var in request.POST:
            print(var)
            print(request.POST[var])
            return HttpResponse('')
    else:
        if username == request.user.username:
            garden = request.user.garden_set.get(name=garden)
            current_url = settings.MEDIA_URL+ "users/" + garden.serial + "/current.png"
            context = {'garden':garden, 'room_name_json': mark_safe(json.dumps(garden.serial)),'MEDIA_URL':settings.MEDIA_URL, "current_url":current_url}
            return render(request,'garden/garden.html', context)
        else: 
            return render(request,'users/no_access.html')

def toggler(request, username=None, garden=None):
    outlet_num = request.POST.get('outlet_num')
    garden_ser = request.POST.get('garden_ser')
    print("Changing outlet for ",garden_ser)
    garden = Garden.objects.get(serial=garden_ser)
    outlet = Outlet.objects.get(number=outlet_num,garden=garden)
    outlet.toggle()
    consumers.toggle_talk(garden_ser, outlet_num, outlet.is_on)
    if outlet.is_on: text = {'button_state':"power"}
    else: text = {'button_state':"power_off"}
    return JsonResponse(text)

def new_garden(request, username=None):
    if request.method == "POST":
        form = CreateGardenForm(request.POST)
        if form.is_valid():
            new_garden = form.save(commit=False)
            new_garden.user = request.user
            new_garden.save()
            for x in range (1,6):
                new_outlet = Outlet(number=x,garden=new_garden)
                new_outlet.assign()
                new_outlet.save()
        return redirect('gardens',username=request.user.username)
    else:
        if username == request.user.username:
            form = CreateGardenForm()
            context = {'form': form}
            return render(request,'garden/new_garden.html', context)
        else: 
            return render(request,'users/no_access.html')

def outlet(request, outlet_num= None, garden = None, username = None):
    if username == request.user.username:
        garden = request.user.garden_set.get(name=garden)
        outlet = garden.outlet_set.get(number=outlet_num)
        context = {'garden':garden, 'outlet':outlet, 'room_name_json': mark_safe(json.dumps(garden.serial))}
        return render(request,'garden/outlet.html', context)
    else: 
        return render(request,'users/no_access.html')
        
def outlet_template(request, username=None, garden=None, outlet_num=None):
    garden = request.user.garden_set.get(name=garden)
    outlet = garden.outlet_set.get(number=outlet_num)
    context = {'garden':garden, 'outlet':outlet}
    return render(request, 'garden/outlet_types/'+str(outlet.style)+'.html', context)

def variable_change(request, username=None, garden=None):
    if request.method == 'POST':
        garden = Garden.objects.get(serial=request.POST['garden_serial'])
        #Update variable as defined in json
        if request.POST['outlet_number'] == "0":
            if request.POST['variable'] != "no_change": 
                setattr(garden, request.POST['variable'], request.POST['new_value'])
                garden.save()
                consumers.box_talk(request.POST)
                return HttpResponse('')
        else:
            outlet = Outlet.objects.get(number=request.POST['outlet_number'], garden = garden)
            if request.POST['variable'] != "no_change": 
                setattr(outlet, request.POST['variable'], request.POST['new_value'])
                outlet.save()
                #Send exact same data to correct box
                consumers.box_talk(request.POST)
        
        # Changes of output based on style
            if outlet.style == "PUMP":
                pump_json = outlet.pump_calculator()
                pump_reader = []
                for key in pump_json:
                    times = pump_json[key]
                    #create nice text for template lstrip and replace help get rid of the zero padding (05:00pm -> 5:00pm)
                    times_string = times['on'].strftime("%I:%M %p").lstrip("0").replace(" 0", " ") + "   to   " + times['off'].strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
                    pump_reader.append(times_string)
                return JsonResponse({"data":pump_reader})
            elif outlet.style == "UVB":
                uvb_start_time, uvb_end_time = outlet.uvb_calculator()
                text = uvb_start_time.strftime("%I:%M:%p").lstrip("0").replace(" 0", " ") + " to " + uvb_end_time.strftime("%I:%M:%p").lstrip("0").replace(" 0", " ")
                return JsonResponse({"data":text})
            else:
                return HttpResponse('')
                
def outlet_finder(garden_serial, outlet_number):
    garden = Garden.objects.get(serial=garden_serial)
    outlet = garden.outlet_set.get(number=outlet_number)
    context = {'garden':garden, 'outlet':outlet}
    return outlet