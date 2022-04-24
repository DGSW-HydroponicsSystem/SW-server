import paho.mqtt.client as mqtt
import json

broker = '3.34.123.190'                      # mqtt broker ip
topic = 'HydroponicsSystem/control'

class mqtt_publish():
  def __init__(self):
    self.mqtt = mqtt.Client('python_hub')    # mqtt Client 오브젝트
    self.mqtt.connect(broker, 1883)          # mqtt broker에 연결
    self.mqtt.loop(2)                        # timeout - 2sec

  def led(self, status):
    if status == 'true' or status == 'True':
      response = {
        'type': 'led',
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
    elif status == 'false' or status == 'False':
      response = {
        'type': 'led',
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행

  def fan(self, status):
    if status == 'true' or status == 'True':
      response = {
        'type': 'fan',
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
    elif status == 'false' or status == 'False':
      response = {
        'type': 'fan',
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행

  def waterpump(self, device, status):
    pumpName = 'waterPump'
    if str(device) == '1' or str(device) == '1':
      pumpName = pumpName + str(device)
    else:
      raise UnboundLocalError
    if status == 'true' or status == 'True':
      response = {
        'type': pumpName,
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
    elif status == 'false' or status == 'False':
      response = {
        'type': pumpName,
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())   # topic & message 발행
