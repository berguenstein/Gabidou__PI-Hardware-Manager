from MqttClient import MqttClient
import time
import threading
from HardwareManager import ledsMeter, servoMotor, sevenSegmentDigit

houseClient = MqttClient("HouseClientConf.config")
consumption = ledsMeter(addressI2C=0x72, isInConsumption=True, valuePeak=6000)
production = ledsMeter(addressI2C=0x71, isInConsumption=False, valuePeak=6000)
display = sevenSegmentDigit()
servoMotor = servoMotor()
servoMotor.changeAngle(0)

class MonThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            time.sleep(10)
            print("solar : " + str(houseClient.getPM3()))
            print("boiler of Heating : " + str(houseClient.getPM2()))
            consumption.calcNbLedOn(houseClient.getPM2())
            production.calcNbLedOn(houseClient.getPM3())
            display.displayString(str(int(houseClient.getPM3())))
            #servoMotor.changeAngle(newAngle)



class MonAutreThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            servoMotor.changeAngle(input("Enter the new angle you want to change\r\n"))



m = MonThread()
m.start()

n = MonAutreThread()
n.start()
