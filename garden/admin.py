# /garden/admin.py
from django.contrib import admin
from .models import Garden, Outlet

admin.site.register(Garden)
admin.site.register(Outlet)
# Register your models here.
