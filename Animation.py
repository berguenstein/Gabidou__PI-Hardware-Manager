from HardwareManager import ledsMeter, servoMotor, sevenSegmentDigit
import time

consumption = ledsMeter(addressI2C=0x72, isInConsumption=True, valuePeak=5000)
production = ledsMeter(addressI2C=0x71, isInConsumption=False, valuePeak=5000)
display = sevenSegmentDigit()


i = 0

while i<4:
    i += 1
    j = 0
    while j<24:
        consumption.changeDisplay(j)
        production.changeDisplay(j)
        j += 1
        time.sleep(0.2)

    print("1 done")
