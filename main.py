from MqttClient import MqttClient
import time
from HardwareManager import ledsMeter, servoMotor, sevenSegmentDigit

houseClient = MqttClient("HouseClientConf.config")
consumption = ledsMeter(addressI2C=0x72, isInConsumption=True, valuePeak=3000)
production = ledsMeter(addressI2C=0x71, isInConsumption=False, valuePeak=3000)
display = sevenSegmentDigit()
servoMotor = servoMotor()
servoMotor.changeAngle(0)

while True:
    time.sleep(10)
    print('Active power export :  ' + str(houseClient.getExportPower()) + ' W')
    print('Active power import :  ' + str(houseClient.getImportPower()) + ' W')
    consumption.changeDisplay(newValue=houseClient.getImportPower())
    production.changeDisplay(newValue=houseClient.getExportPower())
    display.displayString(str(houseClient.getExportPower()))
    deltaPower = houseClient.getImportPower() - houseClient.getExportPower()
    newAngle = (deltaPower*20)/150
    print('New angle : ' + str(newAngle))
    servoMotor.changeAngle(newAngle)
