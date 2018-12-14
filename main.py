from MqttClient import MqttClient
import EnergyLogic
import signal
import time
import threading
from HardwareManager import ledsMeter, servoMotor, sevenSegmentDigit

houseClient = MqttClient("HouseClientConf.config")
logic = EnergyLogic(houseClient)
consumption = ledsMeter(addressI2C=0x72, isInConsumption=True, valuePeak=6000)
production = ledsMeter(addressI2C=0x71, isInConsumption=False, valuePeak=6000)
display = sevenSegmentDigit()
servoMotor = servoMotor()

class MonThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        signal.signal(signal.SIGALRM, logic.logic())
        signal.alarm(10)

    def run(self):
        while(True):
            time.sleep(10)
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
