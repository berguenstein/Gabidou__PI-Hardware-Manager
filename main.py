from MqttClient import MqttClient
import time
import threading
from HardwareManager import ledsMeter, servoMotor, sevenSegmentDigit

houseClient = MqttClient("HouseClientConf.config")
consumption = ledsMeter(addressI2C=0x72, isInConsumption=True, valuePeak=500)
production = ledsMeter(addressI2C=0x71, isInConsumption=False, valuePeak=500)
display = sevenSegmentDigit()
servoMotor = servoMotor()
servoMotor.changeAngle(0)

class MonThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            time.sleep(10)
            print('Active power export :  ' + str(houseClient.getExportPower()) + ' W')
            print('Active power import :  ' + str(houseClient.getImportPower()) + ' W')
            consumption.changeDisplay(newValue=houseClient.getImportPower())
            production.changeDisplay(newValue=houseClient.getExportPower())
            display.displayString(str(houseClient.getExportPower()))
            deltaPower = houseClient.getImportPower() - houseClient.getExportPower()
            newAngle = (deltaPower * 20) / 150
            print('New angle : ' + str(newAngle))
            #servoMotor.changeAngle(newAngle)



class MonAutreThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            servoMotor.adaptAngle(input("type something to test the threading"))



m = MonThread()
m.start()

n = MonAutreThread()
n.start()
