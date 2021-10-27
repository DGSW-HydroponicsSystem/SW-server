from django.urls import path
from . import views

app_name = 'v2'
urlpatterns = [
  path('get_all_sensor/', views.get_all_sensor.as_view(), name='index'),
  path('humidity/', views.humidity.as_view(), name='index'),
  path('temp/', views.temp.as_view(), name='index'),
  path('led/', views.led.as_view(), name='index'),
  path('water/', views.water.as_view(), name='index'),
  path('control_led/', views.control_led.as_view(), name='index'),
  path('control_water/', views.control_water.as_view(), name='index')
]