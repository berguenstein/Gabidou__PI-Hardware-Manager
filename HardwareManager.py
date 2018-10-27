from Adafruit_LED_Backpack import BicolorBargraph24


class consumptionMeter:
    i2cAddress = 0x72
    maxValue = 0
    display1 = 0
    nbLeds = 24
    oldToDisplay = 0

    def __init__(self):
        maxValue = 0
        ## Define the i2c address of the component "segment"
        self.display1 = BicolorBargraph24.BicolorBargraph24(address=self.i2cAddress)
        ## end of definition
        ## Define the begining of the communication and set the brightness
        self.display1.begin()
        self.display1.clear()
        self.display1.set_brightness(7)
        self.display1.write_display()
        ## end of definition

    def changeDisplay(self, newValue):
    #begin of the function
        if (newValue > self.maxValue):
            self.maxValue = newValue

        ratio = float(float(newValue) / float(self.maxValue))
        toDisplay = int(self.nbLeds * ratio)

        if (self.oldToDisplay != toDisplay):
            self.oldToDisplay = toDisplay

            self.display1.clear()
            self.display1.write_display()

            for i in range(0, toDisplay + 1):
                invert = self.nbLeds-i-1
                if (invert > 18):
                    self.display1.set_bar(invert, BicolorBargraph24.GREEN)
                else:
                    if (invert > 10):
                        self.display1.set_bar(invert, BicolorBargraph24.YELLOW)

                    else:
                        if (invert >= 0):
                            self.display1.set_bar(invert, BicolorBargraph24.RED)
                self.display1.write_display()


class productionMeter:
    i2cAddress = 0x72
    maxValue = 0
    display1 = 0
    nbLeds = 24
    oldToDisplay = 0

    def __init__(self):
        maxValue = 0
        ## Define the i2c address of the component "segment"
        self.display1 = BicolorBargraph24.BicolorBargraph24(address=self.i2cAddress)
        ## end of definition
        ## Define the begining of the communication and set the brightness
        self.display1.begin()
        self.display1.clear()
        self.display1.set_brightness(7)
        self.display1.write_display()
        ## end of definition

    def changeDisplay(self, newValue):
        if(newValue > self.maxValue):
            self.maxValue = newValue

        ratio = float(float(newValue)/float(self.maxValue))
        toDisplay = int(self.nbLeds*ratio)

        if(self.oldToDisplay != toDisplay):
            self.oldToDisplay = toDisplay

            self.display1.clear()
            self.display1.write_display()

            for i in range(0,toDisplay+1):
                invert = self.nbLeds-i-1
                if(invert>18):
                    self.display1.set_bar(invert,BicolorBargraph24.RED)
                else:
                    if (invert > 10):
                        self.display1.set_bar(invert, BicolorBargraph24.YELLOW)

                    else:
                        if(invert >= 0):
                            self.display1.set_bar(invert, BicolorBargraph24.GREEN)
                self.display1.write_display()

