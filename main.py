from MqttClient import MqttClient
import time
from HardwareManager import consumptionMeter

houseClient = MqttClient("HouseClientConf.config")

while True:
    time.sleep(10)
    print('Active power export :  ' + str(houseClient.getExportPower()) + ' W')
    print('Active power import :  ' + str(houseClient.getImportPower()) + ' W')
