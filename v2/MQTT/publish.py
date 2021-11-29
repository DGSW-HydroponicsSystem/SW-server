import paho.mqtt.client as mqtt
import json

broker = '13.209.41.37'                      # mqtt broker ip
topic = 'HydroponicsSystem/control'

class mqtt_publish():
  def __init__(self):
    self.mqtt = mqtt.Client('python_hub')    # mqtt Client 오브젝트
    self.mqtt.connect(broker, 1883)          # mqtt broker에 연결
    self.mqtt.loop(2)                        # timeout - 2sec

  def led(self, status):
    if status == 'true':
      response = {
        'type': 'led',
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
    elif status == 'false':
      response = {
        'type': 'led',
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행

  def water(self, status):
    if status == 'true':
      response = {
        'type': 'waterPump',
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
    elif status == 'false':
      response = {
        'type': 'waterPump',
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
