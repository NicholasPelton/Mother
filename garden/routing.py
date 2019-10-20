# garden/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/garden/(?P<serial_number>[^/]+)/$', consumers.GardenLoad),
    url(r'^ws/blog/(?P<serial_number>[^/]+)/$', consumers.BlogLoad),
]