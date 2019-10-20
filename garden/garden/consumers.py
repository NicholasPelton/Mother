# garden/consumers.py
from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import WebsocketConsumer, SyncConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Garden, Outlet
from blog.models import Picture
import json
import os
from django.conf import settings
from django.core.files import File
import datetime
from django.utils.dateparse import parse_date
from time import sleep

class BlogLoad(WebsocketConsumer):

    # Receive message from WebSocket
    def connect(self):
        now = datetime.datetime.now().time()
        self.garden_serial = self.scope['url_route']['kwargs']['serial_number']
        print(self.channel_name, self.garden_serial)
        garden = Garden.objects.get(serial=self.garden_serial)
        async_to_sync(self.channel_layer.group_add)(
            self.garden_serial,
            self.channel_name
        )
        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.garden_serial, # Make sure only the correct box gets it
            {'type' : 'camera_load'}, # Send our fun json
        )


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.garden_serial,
            self.channel_name
        )
    
    def camera_confirmation(self, event):
        garden = Garden.objects.get(serial=self.garden_serial)
        print("Loading Picture")
        json_event=json.dumps(event)
        self.send(text_data=json_event)
        try:
            pic_log = Picture.objects.get(photo="users/"+garden.serial+"/current.png", garden = garden)
        except Exception as e:
            print (e)
            pic_log = Picture(garden=garden)
            pic_log.photo="users/"+garden.serial+"/current.png"
        pic_log.date = datetime.datetime.now()
        pic_log.save()
        
    def camera_load(self,event):
        pass
    
    def togglest(self, event):
        pass


class GardenLoad(WebsocketConsumer):
    # Receive message from WebSocket
    def connect(self):
        now = datetime.datetime.now().time()
        self.garden_serial = self.scope['url_route']['kwargs']['serial_number']
        print(self.channel_name, self.garden_serial)
        garden = Garden.objects.get(serial=self.garden_serial)
        async_to_sync(self.channel_layer.group_add)(
            self.garden_serial,
            self.channel_name
        )
        self.accept()
        
        if time_to_min(garden.last_load) > time_to_min(now) : garden.last_load = datetime.time(0,0,0)
        if time_to_min(garden.last_load)+1 < time_to_min(now) :   
            async_to_sync(self.channel_layer.group_send)(
                self.garden_serial, # Make sure only the correct box gets it
                {'type' : 'garden_load'}, # Send our fun json
            )
        else:
            print("Loading too early!")
            
    

    def garden_load(self, event):
        print("trying to talk to box...")
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.garden_serial,
            self.channel_name
        )

    
    def load_data(self, event):
        print("Loading data from box!")
        async_to_sync(self.channel_layer.group_add)(self.garden_serial,self.channel_name)
        garden = Garden.objects.get(serial=self.garden_serial)
        garden.last_load = datetime.datetime.now()
        for key in event['garden_stuff']['fields']:
            if key != 'serial' and key != 'name':
                try:
                    setattr(garden,key, event['garden_stuff']['fields'][key])
                except: print(key," was not in variables")
        garden.save()
        
        for x in range (1,6):
            outlet = Outlet.objects.get(garden=garden, number=x )
            was_on = outlet.is_on
            outlet_data = 'outlet_'+str(x)+'_stuff'
            for key in event[outlet_data]['fields']:
                if key != 'garden':
                    try:
                        setattr(outlet,key, event[outlet_data]['fields'][key])
                    except: print(key," was not in variables")
            outlet.save()
            if was_on != outlet.is_on:
                async_to_sync(self.channel_layer.group_send)(
                    self.garden_serial, # Make sure only the correct box gets it
                    {
                        'type' : 'togglest',
                        'outlet' : x,
                        'is_on' : outlet.is_on,
                    }
                    , # Send our fun json
                )
                print("Phew, this should automatically update what has changed in the garden")
            
        #Now loop to get the pictures    
        x=1
        #print (event)
        while x<100:
            try:
                
                # We don't need to replace the current pictures here in garden load
                if event['picture update '+str(x)]['fields']['photo'] == 'users/'+garden.serial+'/current.png':
                    print(event['picture update '+str(x)]['fields']['photo'])
                    print("We don't need to save the current pictures")
                else:
                    pic_log = Picture(garden=garden)
                    print ("ok, we now have a new picture object")
                    for key in event['picture update '+str(x)]['fields']:
                        setattr(pic_log, key, event['picture update '+str(x)]['fields'][key])
                        print (key,": ",event['picture update '+str(x)]['fields'][key])
                    pic_current = Picture.objects.get(photo="users/"+garden.serial+"/current.png", garden = garden)
                    print (pic_log.date, " and ", pic_current.date)
                    if isinstance(pic_log.date,str):pic_log.date = parse_date(pic_log.date)
                    if isinstance(pic_current.date,str):pic_current.date = parse_date(pic_current.date)
                    if pic_log.date == pic_current.date:
                        print ("THE DATES ARE THE SAME DAMMIT!")
                        pic_log.comments = pic_current.comments
                        pic_current.comments = ""
                        print ("I have inherited the current comments! They are mine!")
                        pic_current.save()
                    pic_log.save()
            except:
                break
            x = x + 1 # Failsafe to prevent infinate loop, you should really check on your plant after 100 days
            
        
    
    def togglest(self, event):
        print("WE have a timer based toggle!")
        json_event=json.dumps(event)
        self.send(text_data=json_event)
    
    def toggle(self,event):
        pass
    
    def data_exchange(self, event):
        print("at least this data exchange works")
    
    def camera_load(self, event):
        pass
    
    def camera_confirmation(self,event):
        pass
    
''' UPDATE CODE!! DON'T DO IT ACCIDENTALLY!        
def update_mode_for_real():
    new_git = "https://github.com/gradeahonky/motherbrainLED.git"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        "change_detect",
        {'type' : "update_mode_for_real", 'new_git' : new_git}, # Send our fun update json to all boxes
)
'''



        
def box_talk(json):
    print('I AM BOX TALK')
    channel_layer = get_channel_layer()
    garden_serial = json['garden_serial']
    print(json['type'])
    async_to_sync(channel_layer.group_send)(
        garden_serial, # Make sure only the correct box gets it
        json, # Send our fun json
    )

def toggle_talk(garden_serial, outlet_number, is_on):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        garden_serial, # Make sure only the correct box gets it
        {
            'type' : 'toggle',
            'outlet' : outlet_number,
            'is_on' : is_on,
        }
        , # Send our fun json
    )
    

def time_to_min(time):
    minutes = time.hour * 60 + time.minute
    return minutes