from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt  # csrf 비활성화 라이브러리
from django.utils.decorators import method_decorator  # csrf 비활성화를 위한 메서드, 클래스 데코레이터
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from .MQTT.publish import *
from .MQTT.subscribe import *
from .models import *

from .__init__ import recv_stat, recv_module


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
        sensorValue = recv_stat()
        returnValue = {
            'temp_1': sensorValue['temp_1'],
            'temp_2': sensorValue['temp_2'],
            'humidity_1': sensorValue['humidity_1'],
            'humidity_2': sensorValue['humidity_2'],
            'sunlight_1': sensorValue['sunlight_1'],
            'sunlight_2': sensorValue['sunlight_2'],
            'water_temp_1': sensorValue['water_temp_1'],
            'water_temp_2': sensorValue['water_temp_2'],
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
class get_all_module_status(View):
    def get(self, request):
        sensorValue = recv_module()
        returnValue = {
            'led_status': sensorValue['led_status'],
            'water_pump_status_1': sensorValue['water_pump_status_1'],
            'water_pump_status_2': sensorValue['water_pump_status_2'],
            'fan_status': sensorValue['fan_status'],
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
        sensorValue = recv_stat()
        returnValue = {
            'temp_1': sensorValue['temp_1'],
            'temp_2': sensorValue['temp_1'],
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class humidity(View):
    def get(self, request):
        sensorValue = recv_stat()
        returnValue = {
            'humidity_1': sensorValue['humidity_1'],
            'humidity_2': sensorValue['humidity_2']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class sunlight(View):
    def get(self, request):
        sensorValue = recv_stat()
        returnValue = {
            'sunlight_1': sensorValue['sunlight_1'],
            'sunlight_2': sensorValue['sunlight_2']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water_temp(View):
    def get(self, request):
        sensorValue = recv_stat()
        returnValue = {
            'water_temp_1': sensorValue['water_temp_1'],
            'water_temp_2': sensorValue['water_temp_2']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water_level(View):
    def get(self, request):
        sensorValue = recv_stat()
        returnValue = {
            'water_level': sensorValue['water_level']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class water_ph(View):
    def get(self, request):
        sensorValue = recv_stat()
        returnValue = {
            'water_ph': sensorValue['water_ph']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)


@method_decorator(csrf_exempt, name='dispatch')
class led(View):
    def get(self, request):
        sensorValue = recv_module()
        returnValue = {
            'led_status': sensorValue['led_status']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)

    def post(self, request):
        try:
            if request.META['CONTENT_TYPE'] == 'application/json':
                request = json.loads(request.body)
                led_status = request['status']
            else:
                led_status = request.POST['status']
            mqtt = mqtt_publish()
            mqtt.led(led_status)
            returnValue = {
                "status": 200,
                "detail": "OK",
                "data": {}
            }
            return JsonResponse(returnValue, status=200)

        except Exception as E:
            return HttpResponse('UNKNOWN SERVER ERROR ACCORDED', status=500)


@method_decorator(csrf_exempt, name='dispatch')
class waterpump(View):
    def get(self, request):
        sensorValue = recv_module()
        returnValue = {
            'water_pump_status_1': sensorValue['water_pump_status_1'],
            'water_pump_status_2': sensorValue['water_pump_status_2']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }

        return JsonResponse(returnValue)

    def post(self, request):
        # try:
        if request.META['CONTENT_TYPE'] == 'application/json':
            request = json.loads(request.body)
            pump_status = request['status']
            pump_number = request['pump_number']
        else:
            try:
                pump_status = request.POST['status']
                pump_number = request.POST['pump_number']
            except MultiValueDictKeyError:
                returnValue = {
                    "status": 400,
                    "detail": "Some Value is missing",
                    "data": {}
                }
                return JsonResponse(returnValue, status=200)
        mqtt = mqtt_publish()
        try:
            mqtt.waterpump(pump_number, pump_status)
        except UnboundLocalError:
            return JsonResponse({
                "status": 400,
                "detail": "Wrong Pump number",
                "data": {}
            })
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": {}
        }
        return JsonResponse(returnValue, status=200)
        # except Exception as E:
        #     return HttpResponse('UNKNOWN SERVER ERROR ACCORDED', status=500)


@method_decorator(csrf_exempt, name='dispatch')
class fan(View):
    def get(self, request):
        sensorValue = recv_module()
        returnValue = {
            'fan_status': sensorValue['fan_status']
        }
        returnValue = {
            "status": 200,
            "detail": "OK",
            "data": returnValue
        }
        return JsonResponse(returnValue)

    def post(self, request):
        try:
            if request.META['CONTENT_TYPE'] == 'application/json':
                request = json.loads(request.body)
                fan_status = request['status']
            else:
                fan_status = request.POST['status']
            mqtt = mqtt_publish()
            mqtt.fan(fan_status)

            returnValue = {
                "status": 200,
                "detail": "OK",
                "data": {}
            }
            return JsonResponse(returnValue, status=200)

        except Exception as E:
            return HttpResponse('UNKNOWN SERVER ERROR ACCORDED', status=500)