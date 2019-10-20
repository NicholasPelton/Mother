# gardens/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('gardens', views.gardens, name='gardens'),
    path('new_garden', views.new_garden, name='new_garden'),
    path('<str:garden>/', views.garden, name='garden'),
    path('toggler', views.toggler, name='toggler'),
    path('<str:garden>/blog', include('blog.urls')),
    path('<str:garden>/<str:outlet_num>', views.outlet, name='outlet'),
    path('<str:garden>/<str:outlet_num>/outlet_template', views.outlet_template, name='outlet_template'),
    path('variable_change',views.variable_change,name='variable_change'),
#    path('update_mode_for_real', views.update_mode_for_real) This is a fake path for the update thing

]