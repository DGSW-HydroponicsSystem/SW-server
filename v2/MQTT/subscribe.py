import time
import paho.mqtt.client as mqtt
import json


class MQTT:
    def __init__(self):
        self.broker = '3.34.123.190'
        self.port = 1883
        self.topic = 'HydroponicsSystem/stat'  # 하드웨어 쪽과 상의 후 추후 변경
        self.client = None

        # sensor Value
        self.Key = int()
        self.temperature1 = int()
        self.temperature2 = int()
        self.humidity1 = int()
        self.humidity2 = int()
        self.sunlight1 = int()
        self.sunlight2 = int()
        self.water_temp1 = int()
        self.water_temp2 = int()
        self.water_level = int()
        self.water_ph = float()
        self.led_status = int()
        self.pump_status = int()
        self.fan_status = int()


    def connect_mqtt(self) -> mqtt:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print('Connected to MQTT Broker!')
            else:
                print('Failed to connect, return code %d\n', rc)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt):
        def on_message(client, userdata, msg):
            recv = msg.payload.decode()
            data = json.loads(recv)
            if data:
                self.Key = data['Key']
                if self.Key == 0:
                    self.temperature1 = data['temperature1']
                    self.temperature2 = data['temperature2']
                    self.humidity1 = data['humidity1']
                    self.humidity2 = data['humidity2']
                    self.sunlight1 = data['sunlight1']
                    self.sunlight2 = data['sunlight2']
                    self.water_temp1 = data['watertemp1']
                    self.water_temp2 = data['watertemp2']
                    self.water_level = data['waterlevel']
                    self.water_ph = data['waterph']
                else:
                    self.led_status = data['ledstat']
                    self.pump_status = data['waterpumpstat']
                    self.fan_status = data['fanstat']
            else:
                print('no data...')

        client.subscribe(self.topic)
        client.on_message = on_message

    def run(self):
        self.client = self.connect_mqtt()
        self.subscribe(self.client)
        self.client.loop_start()
        print('run!!')
        time.sleep(1)
        self.get_data()

    def get_data(self):
        returnValue_Key0 = {
            'Key': 0,
            'temp_1': {'value': 0},
            'temp_2': {'value': 0},
            'humidity_1': {'value': 0},
            'humidity_2': {'value': 0},
            'sunlight_1': {'value': 0},
            'sunlight_2': {'value': 0},
            'water_temp_1': {'value': 0},
            'water_temp_2': {'value': 0},
            'water_level': {'value': 0},
            'water_ph': {'value': 0.0},
        }
        returnValue_Key1 = {
            'Key': 1,
            'led_status': {'value': False},
            'water_pump_status': {'value': False},
            'fan_status': {'value': False}
        }

        if self.Key == 1:
            returnValue_Key1['Key'] = self.Key
            returnValue_Key1['led_status']['value'] = True if self.led_status == 1 else False
            returnValue_Key1['water_pump_status']['value'] = True if self.pump_status == 1 else False
            returnValue_Key1['fan_status']['value'] = True if self.fan_status == 1 else False

            return returnValue_Key1
        else:
            returnValue_Key0['Key'] = self.Key
            returnValue_Key0['temp_1']['value'] = self.temperature1
            returnValue_Key0['temp_2']['value'] = self.temperature2
            returnValue_Key0['humidity_1']['value'] = self.humidity1
            returnValue_Key0['humidity_2']['value'] = self.humidity2
            returnValue_Key0['sunlight_1']['value'] = self.sunlight1
            returnValue_Key0['sunlight_2']['value'] = self.sunlight2
            returnValue_Key0['water_temp_1']['value'] = self.water_temp1
            returnValue_Key0['water_temp_2']['value'] = self.water_temp2
            returnValue_Key0['water_level']['value'] = self.water_level
            returnValue_Key0['water_ph']['value'] = self.water_ph

            return returnValue_Key0
