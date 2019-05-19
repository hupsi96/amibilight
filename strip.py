from neopixel import *
import logging
import time
import numpy as np
class strip_config:


    LED_COUNT      = 20      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0
    LED_STRIP      = ws.SK6812_STRIP_RGBW # setup for new strip

    #define strip globaly and set default values
    global strip
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP) #default setting """Adafruit_NeoPixel"""

    #confic logging module
    logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')

    #define global List to store Colurs for all LEDs
    global stripStatusList

    #fadeTime for all fading functions - default value "medium"
    global fadeTime
    

    #testMode deactivates all Show calls to avaid turning on and off the LES remotely
    global testMode

    #Status if On command shold be executed
    global switchStatus
    #Constructor
    def __init__(self, num, pin):
        # config strip
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

        self.testMode = False

        self.fadeTime = 0.005

        # List to store current color values
        #The tupel show the values (brightness,red,green,blue,brightness)
        self.stripStatusList = [[0,0,0,0]] * num
        self.switchStatus = True
        #Test Color
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,100,100,100)
            self.stripStatusList[x] = [0,100,100,100,10]
        strip.setBrightness(10)
        self.switchStatus = True
        if not self.testMode:
            strip.show()
            time.sleep(1)
        self.fadeStripBrightness(0,True)
        strip.show()

	for x in range(strip.numPixels()):
		strip.setPixelColorRGB(x,100,0,0)
	strip.show()
        #test
        #print(self.ColorRGB(0,100,150,200))
        #print(bin(self.ColorRGB(0,100,150,200)))
        #print(self.ColorNum(self.ColorRGB(0,100,150,200)))
        #self.stripStatusList[10] = [0,255,200,100,10]
        #self.stripStatusList[20] = [0,0,0,255,10]
        #self.test_Pixel_numbers()

        

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
            self.stripStatusList[x] = [0,0,0,0,0]
        strip.show()
        print("Done")

    #Sets the brightness of the whole strip | update is a bool to indicate 
    #if the status List should be updated or not
    #this is set to false when the strip is switched off in order
    #to store the last brightness value of the strip
    def fadeStripBrightness(self,value,update):
        #current brightness of the whole strip
        currentBirghtness = strip.getBrightness()
        print(self.fadeTime)

        #steps needed to fade strip
        delta = currentBirghtness - value

        #value for for-loop - has to be positiv
        boundary = delta if delta > 0 else (delta * (-1))
        for x in range(0,boundary +1):
            if delta < 0:
                strip.setBrightness(currentBirghtness+x)
            elif delta > 0:
                strip.setBrightness(currentBirghtness-x)
            if not self.testMode:
                strip.show()
            time.sleep(self.fadeTime)
        logging.info('Brightness set to: +' + str(value))
        if update:
            for x in range(strip.numPixels()):
                current = self.stripStatusList[x]
                current[4] = int(value)
                self.stripStatusList[x] = current
        print("Done")

    def turn_on_animation (self):
        for x in range(strip.numPixels()):
            strip.setBrightness(self.stripStatusList[x][4])
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()
        for y in range(1,3):
            for x in range(strip.numPixels()):
                current = self.stripStatusList[x]
                if y == 1:
                    strip.setPixelColorRGB(x,int(current[2] * 0.5),int(current[1] * 0.5),int(current[3] * 0.5))
                    #strip.setBrightness(int(current[4] * 0.5))
                    #print(int(current[1] * 0.5))
                else:
                    strip.setPixelColorRGB(x,current[2],current[1],current[3])
                    #strip.setBrightness(current[4])
                    #print(current[1])
                if not self.testMode:
                    strip.show()
                time.sleep(self.fadeTime)
        logging.info('Animation done')
        print("Done")

    def switch(self, value):
        if value == "OFF":
            self.fadeStripBrightness(0,False)
            strip.show()
            logging.info('Strip switched off')
            self.switchStatus = False
        elif value == "ON":
            if not self.switchStatus:
                self.turn_on_animation()
                self.switchStatus = True
            print("Done")

    def fadeColor(self,red,green,blue):
        delta = 0

        #Define max fade range
        for x in self.stripStatusList:
            if abs(red - x[1]) > abs(delta):
                delta = red - x[1]
            if abs(green - x[2]) > abs(delta):
                delta = green - x[2]
            if abs(blue - x[3]) > abs(delta):
                delta = blue - x[3]
        #set Color steop by step in delta+1 steps to final value
        if delta != 0:
            for y in range(abs(delta)+1):
                for x in range(strip.numPixels()):
                    red_old = self.stripStatusList[x][1]
                    green_old = self.stripStatusList[x][2]
                    blue_old = self.stripStatusList[x][3]
                    red_new = float(red_old) + ((float(red - red_old)/float(abs(delta)))*float(y))
                    green_new = float(green_old) + ((float(green - green_old)/float(abs(delta)))*float(y))
                    blue_new = float(blue_old) + ((float(blue - blue_old)/float(abs(delta)))*float(y))
                    #strip.setPixelColorRGB takes values not RGB but GRB
                    strip.setPixelColorRGB(x, int(green_new), int(red_new),int(blue_new))
                    #testing output
                    #if x == 1 or x == 10 or x == 20:
                        #print(x)
                        #print(str(red_new)+","+ str(green_new)+"," + str(blue_new))
                if not self.testMode:
                    strip.show()
                #time.sleep(fadeTime/8)
        
        #adjust stored r,g,b values
        for x in range(strip.numPixels()):
            current = self.stripStatusList[x]
            current[1] = red
            current[2] = green
            current[3] = blue
            self.stripStatusList[x] = current
        print("Done")
    
    def setFadeSpeed(self,level):
        if level == "fast":
            self.fadeTime = 0.0005
        elif level == "medium":
            self.fadeTime = 0.005
        elif level == "slow":
            self.fadeTime = 0.03


    def setWhiteValue(self, value):
        rng = 500 - 152
        factor = 255.0/rng
        print(factor)
        trueValue = int(value) - 153
        print(trueValue)
        setValue = factor * float(trueValue)
        print(setValue)

        for x in range(strip.numPixels()):
            strip.setPixelColor(x, Color(0,0,0,int(setValue)))
        strip.show()


    def test_Pixel_numbers (self):
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,37,74,0)
            strip.show()
            print(x)
            time.sleep(0.05)
        


    def ColorRGB (self,white,red,green,blue):
        return (white << 24) | (red << 16)| (green << 8) | blue

    def ColorNum (self,num):
        #using Binary logic to decode numeric input to (white,red,green.blue) tupel
        # bin of num is a 32 bit sequemce
        # using logical & to get bit sequence of the first, second, third and fourth
        # block of 8 bit e.g.
        # 10100010010101010101110000 & 00000000111111110000000000000000

        white = (4278190080 & num) >> 24
        red = (16711680 & num) >> 16
        green = (65280 & num) >> 8
        blue = 255 & num
        return [int(white),int(red),int(green),int(blue)]
