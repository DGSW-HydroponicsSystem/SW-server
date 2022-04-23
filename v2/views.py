from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt  # csrf 비활성화 라이브러리
from django.utils.decorators import method_decorator  # csrf 비활성화를 위한 메서드, 클래스 데코레이터
from django.core.exceptions import ObjectDoesNotExist
from .MQTT.publish import *
from .MQTT.subscribe import *
from .models import *

from .__init__ import recv


@method_decorator(csrf_exempt, name='dispatch')
class cropInfo_all_API(View):
    def get(self, request):
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": {
                "crops": []
            }
        }
        try:
            crop = cropModel.objects.all()
            crop = list(crop)
        except ObjectDoesNotExist:
            return JsonResponse(returnValue)
        for x in crop:
            cropValue = {
                "pk": x.primaryKey,
                "name": x.name,
                "image": x.image.url
            }
            returnValue["data"]["crops"].append(cropValue)
        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class currCropInfo_API(View):
    def get(self, request):
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": {
                "pk": 0,
                "name": "",
                "image_url": "",
                "content": ""
            }
        }
        try:
            crop = currCrop.objects.all()
            crop = list(crop)[0]
        except (ObjectDoesNotExist, IndexError):
            return JsonResponse(returnValue)
        returnValue["data"]["pk"] = crop.crop.primaryKey
        returnValue["data"]["name"] = crop.crop.name
        returnValue["data"]["image_url"] = crop.crop.image.url
        returnValue["data"]["content"] = crop.crop.info
        return JsonResponse(returnValue)

    def put(self, request):
        try:
            pk = request.GET['pk']
        except (KeyError, ValueError):
            return JsonResponse({"status": 400, "detail": 'Some Values are missing', "data": {}}, status=400)
        try:
            crop_Model = currCrop.objects.all()
            crop_Model = list(crop_Model)[0]
        except (ObjectDoesNotExist, IndexError):
            try:
                crop_Model = currCrop(crop=cropModel.objects.get(primaryKey=int(pk)))
                crop_Model.save()
            except ObjectDoesNotExist:
                return JsonResponse({"status": 401, "detail": 'There is no crop', "data": {}}, status=401)
        try:
            crop_Model.crop = cropModel.objects.get(primaryKey=int(pk))
            crop_Model.save()
            return JsonResponse({"status": 200, "detail": 'OK', "data": {}}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"status": 401, "detail": 'There is no crop', "data": {}}, status=401)



@method_decorator(csrf_exempt, name='dispatch')
class get_all_sensor(View):
    def get(self, request):
        sensorValue = recv()
        returnValue = {
            'humidity_1': sensorValue['humidity1'],
            'humidity_2': sensorValue['humidity2'],
            'temp_1': sensorValue['temperature1'],
            'temp_2': sensorValue['temperature2'],
            'led_status': sensorValue['led_status'],
            'water_pump_status': sensorValue['water_status'],
            'fan_status': sensorValue['fan_status'],
            'sunlight': sensorValue['sunlight'],
            'water_temp': sensorValue['water_temp'],
            'water_level': sensorValue['water_level'],
            'water_ph': sensorValue['water_ph']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
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
class sunlight(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': senserValue['sunlight']
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class waterpump(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': bool(senserValue['waterpump'])
        }

        return JsonResponse(returnValue)

    def post(self, request):
        if request.META['CONTENT_TYPE'] == 'application/json':
            request = json.loads(request.body)
            pump_status = request['status']
        else:
            pump_status = request.POST['status']
        mqtt = mqtt_publish()
        mqtt.water(pump_status)
        return HttpResponse('OK', status=200)


@method_decorator(csrf_exempt, name='dispatch')
class water_temp(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': int(senserValue['water_temp'])
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water_level(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': int(senserValue['water_level'])
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water_ph(View):
    def get(self, request):
        senserValue = recv()
        returnValue = {
            'value': float(senserValue['water_ph'])
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
