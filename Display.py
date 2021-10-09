import numpy as np
from datetime import datetime as dt
import math

class Display:
    def __init__(self):
        self.width = 11
        self.height = 10
        self.array = np.zeros((self.width, self.height))
        self.resetMask()
        self.time = 0.0
        
        self.hourswitcher = {
            1: self.einuhr,
            2: self.zweiuhr,
            3: self.dreiuhr,
            4: self.vieruhr,
            5: self.fuenfuhr,
            6: self.sechsuhr,
            7: self.siebenuhr,
            8: self.achtuhr,
            9: self.neunuhr,
            10: self.zehnuhr,
            11: self.elfuhr,
            12: self.zwoelfuhr
        }
        
        self.minuteswitcher = {
            5: [self.fuenf, self.nach],
            10: [self.zehn, self.nach],
            15: [self.viertel, self.nach],
            20: [self.zwanzig, self.nach],
            25: [self.fuenf, self.vor, self.halb],
            30: [self.halb],
            35: [self.fuenf, self.nach, self.halb],
            40: [self.zwanzig, self.vor],
            45: [self.viertel, self.vor],
            50: [self.zehn, self.vor],
            55: [self.fuenf, self.vor]

        }

    def resetMask(self):
        self.mask = np.zeros((self.width, self.height))
        
    def encode(self, time):
        hour = int(time.strftime('%-I'))
        minute = int(time.strftime('%-M'))

        min5 = int(math.floor(minute / 5) * 5)

        self.resetMask()
        self.es()
        self.ist()
            
        # Display Minute in 5min steps with "vor" / "nach" / "halb" etc.
        for word in self.minuteswitcher[min5]:
            word()

        # Increase hour count for half hour times
        if min5 > 20:
            hour += 1

        # Display hour and hour+1 if min5 allows "halb"-hour
        self.hourswitcher[hour]() 
        
    def es(self):
        self.mask[0 , 0:2] = 1

    def ist(self):
        self.mask[0 , 3:6] = 1
            
    def fuenf(self):
        self.mask[0, 7:] = 1
        self.mask[1, 0] = 1
        
    def zehn(self):
        self.mask[1, 1:5] = 1
        
    def fuenfzehn(self):
        self.mask[2, 6:] = 1
        self.mask[3, 0:3] = 1
        
    def viertel(self):
        self.mask[2, 6:] = 1
        self.mask[3, 0:3] = 1 

    def dreiviertel(self):
        self.mask[2, 2:6] = 1
        self.viertel()

    def zwanzig(self):
        self.mask[1, 5:] = 1
        self.mask[2, 0:2] = 1
        
    def halb(self):
        self.mask[4, 4:8] = 1
        
    def vor(self):
        self.mask[3, 3:6] = 1
        
    def nach(self):
        self.mask[4, 0:4] = 1

    def einuhr(self):
        self.mask[5, 5:9] = 1
        
    def zweiuhr(self):
        self.mask[6, 2:6] = 1

    def dreiuhr(self):
        self.mask[6, 6:] = 1
        
    def vieruhr(self):
        self.mask[8, 4:8] = 1
    
    def fuenfuhr(self):
        self.mask[5, 1:5] = 1

    def sechsuhr(self):
        self.mask[7, 7:] = 1
        self.mask[8, 0:2] = 1

    def siebenuhr(self):
        self.mask[8, 8:] = 1
        self.mask[9, 0:4] = 1

    def achtuhr(self):
        self.mask[8, 4:8] = 1

    def neunuhr(self):
        self.mask[10, 2:6] = 1

    def zehnuhr(self):
        self.mask[9, -1] = 1
        self.mask[10, 0:3] = 1

    def elfuhr(self):
        self.mask[4, -1] = 1
        self.mask[5, :2] = 1

    def zwoelfuhr(self):
        self.mask[9, 4:8] = 1

    def uhr(self):
        self.mask[-1, 8:] = 1

    def map(self):
        mapString = "ESKISTAFÜNFZEHNZWANZIGDREIVIERTELVORFUNKNACHHALBAELFÜNFEINSXAMZWEIDREIPMJVIERSECHSNLACHTSIEBENZWÖLFZEHNEUNKUHR"
        self.array = np.reshape([c for c in mapString], self.array.shape)

    def test(self):
        self.map()
        self.encode(dt.now())
        #self.newarray = np.zeros((self.width + 1 , self.height + 1), dtype=str)
        #self.newarray[: , 0] = range(self.width + 1)
        #self.newarray[0 , :] = range(self.height + 1)
        #self.newarray[1: , 1: ] = self.array
        #print(self.newarray)
        print(np.where(self.mask, self.array, ""))


if __name__ == "__main__":
    myDisplay = Display()
    myDisplay.test()
