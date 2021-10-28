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
    self.temp = None
    self.humidity = None
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
        self.temp = j['temperature']
        self.humidity = j['humidity']
        self.led_status = j['led']
        self.water_status = j['waterpump']
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
    if self.temp == None and self.humidity == None and self.led_status == None and self.water_status == None:
      returnValue = {
        'temp': 0,
        'temp_status': 0,
        'humidity': 0,
        'humidity_status': 0,
        'led_status': 0,
        'water_status': 0
      }
      return returnValue

    else:
      returnValue = {
        'temp': self.temp,
        'humidity': self.humidity,
        'led_status': self.led_status,
        'water_status': self.water_status
      }

      if self.temp < 20:
        returnValue['temp_status'] = -1
      elif (self.temp >= 20) and (self.temp <= 25):
        returnValue['temp_status'] = 0
      else:
        returnValue['temp_status'] = 1

      if self.humidity < 40:
        returnValue['humidity_status'] = -1
      elif (self.humidity >= 40) and (self.humidity <= 60):
        returnValue['humidity_status'] = 0
      else:
        returnValue['humidity_status'] = 1

      return returnValue