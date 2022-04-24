from django.urls import path
from . import views

app_name = 'v2'
urlpatterns = [
  path('user/crops/', views.currCropInfo_API.as_view(), name='index'),
  path('user/crops/all/', views.cropInfo_all_API.as_view(), name='index'),
  path('get_all_sensor/', views.get_all_sensor.as_view(), name='index'),
  path('get_all_module_status/', views.get_all_sensor.as_view(), name='index'),
  path('temp/', views.temp.as_view(), name='index'),
  path('humidity/', views.humidity.as_view(), name='index'),
  path('sunlight/', views.sunlight.as_view(), name='index'),
  path('watertemp/', views.water_temp.as_view(), name='index'),
  path('waterlevel/', views.water_level.as_view(), name='index'),
  path('waterph/', views.water_ph.as_view(), name='index'),
  path('led/', views.led.as_view(), name='index'),
  path('water/', views.waterpump.as_view(), name='index'),
  path('fan/', views.fan.as_view(), name='index'),
]
