from .MQTT import subscribe as mqtt

mqtt = mqtt.MQTT()

def recv():
  sensorValue = mqtt.run()
  return sensorValue