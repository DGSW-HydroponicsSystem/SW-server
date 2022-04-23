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
        self.temperature1 = None
        self.temperature2 = None
        self.humidity1 = None
        self.humidity2 = None
        self.led_status = None
        self.water_status = None
        self.sunlight = None
        self.water_temp = None
        self.water_level = None
        self.water_ph = None


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
                self.temperature1 = data['temperature1']
                self.temperature2 = data['temperature2']
                self.humidity1 = data['humidity1']
                self.humidity2 = data['humidity2']
                self.led_status = data['led']
                self.water_status = data['waterpump']
                self.fan_status = data['fan']
                self.sunlight = data['sunlight']
                self.water_temp = data['watertemp']
                self.water_level = data['waterlevel']
                self.water_ph = data['waterph']
                # print('this if got : {}', format(j))  # 가져온 값 출력
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
        if self.temperature1 == None or self.temperature2 == None or self.humidity1 == None or \
            self.humidity2 == None or self.led_status == None or self.water_status == None or \
            self.sunlight == None or self.water_temp == None or self.water_level == None or \
            self.water_ph == None:
            returnValue = {
                'temperature1': {'value': 0},
                'temperature2': {'value': 0},
                'humidity1': {'value': 0},
                'humidity2': {'value': 0},
                'led_status': {'status': False},
                'water_status': {'status': False}
            }
        else:
            returnValue = {
                'temperature1': {'value': self.temperature2},
                'temperature2': {'value': self.temperature2},
                'humidity1': {'value': self.humidity2},
                'humidity2': {'value': self.humidity2},
                'led_status': {'status': True if self.led_status else False},
                'water_status': {'status': True if self.water_status else False}
            }

        return returnValue
