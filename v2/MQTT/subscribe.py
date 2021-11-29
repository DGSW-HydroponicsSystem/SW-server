import time
import paho.mqtt.client as mqtt
import json


class MQTT:
    def __init__(self):
        self.broker = '13.209.41.37'
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
            j = json.loads(recv)
            if j:
                self.temperature1 = j['temperature1']
                self.temperature2 = j['temperature2']
                self.humidity1 = j['humidity1']
                self.humidity2 = j['humidity2']
                self.led_status = j['led']
                self.water_status = j['waterpump']
                print('this if got : {}', format(j))  # 가져온 값 출력
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
        if self.temperature1 == None or self.temperature2 == None or self.humidity1 == None or self.humidity2 == None or self.led_status == None or self.water_status == None:
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
                'temperature1': {'value': self.temperature1},
                'temperature2': {'value': self.temperature2},
                'humidity1': {'value': self.humidity1},
                'humidity2': {'value': self.humidity2},
                'led_status': {'status': self.led_status},
                'water_status': {'status': self.water_status}
            }

        return returnValue
