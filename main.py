from MqttClient import MqttClient
import time
from HardwareManager import consumptionMeter

houseClient = MqttClient("HouseClientConf.config")

while(True):
    time.sleep(0.2)