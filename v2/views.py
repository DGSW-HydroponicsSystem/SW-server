from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt  # csrf 비활성화 라이브러리
from django.utils.decorators import method_decorator  # csrf 비활성화를 위한 메서드, 클래스 데코레이터
from .MQTT.publish import *
from .MQTT.subscribe import *

from .__init__ import recv


@method_decorator(csrf_exempt, name='dispatch')
class get_all_sensor(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'humidity_1': {
                'value': senserValue['humidity1']
            },
            'humidity_2': {
                'value': senserValue['humidity2']
            },
            'temp_1': {
                'value': senserValue['temperature1']
            },
            'temp_2': {
                'value': senserValue['temperature2']
            },
            'led_status': {
                'status': senserValue['led_status']
            },
            'water_pump_status': {
                'status': senserValue['water_status']
            }
        }
        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class temp(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'status': senserValue['temp_status'],
            'value': senserValue['temp']
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class humidity(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'status': senserValue['humidity_status'],
            'value': senserValue['humidity']
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class led(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': senserValue['led_status']
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': senserValue['water_status']
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class control_water(View):
    def post(self, request):
        if request.META['CONTENT_TYPE'] == 'application/json':
            request = json.loads(request.body)
            water_status = request['status']
        else:
            water_status = request.POST['status']
        mqtt = mqtt_publish()
        mqtt.water(water_status)
        return HttpResponse('OK', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class control_led(View):
    def post(self, request):
        try:
            if request.META['CONTENT_TYPE'] == 'application/json':
                request = json.loads(request.body)
                led_status = request['status']
            else:
                led_status = request.POST['status']
            mqtt = mqtt_publish()
            mqtt.led(led_status)
            return HttpResponse('OK', status=200)

        except:
            return HttpResponse('UNKNOWN SERVER ERROR ACCORDED', status=500)
