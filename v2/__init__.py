from .MQTT import subscribe as mqtt

mqtt_stat = mqtt.MQTT_STAT()
mqtt_module = mqtt.MQTT_MODULE()
mqtt_stat.run()
mqtt_module.run()

def recv_stat():
  sensorValue = mqtt_stat.get_data()
  return sensorValue

def recv_module():
  sensorValue = mqtt_module.get_data()
  return sensorValue
