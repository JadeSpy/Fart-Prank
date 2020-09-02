from playsound import playsound
import time
import inspect
import random
import win32gui
import win32api
class availableCommands():
    global identifier
    identifier = 1
    def help(function=False):
        if function:
            if not function in dir(availableCommands):
                print("Function does not exist:",function)
                return
            print(function)
            print("Function arguments:",inspect.getargspec(eval("availableCommands."+function))[0])
        else:
            for sayFunction in dir(availableCommands):
                if(sayFunction[0]!="_"):
                    print(sayFunction, inspect.getargspec(eval("availableCommands."+sayFunction))[0])
        return("no send")
    def playfart(fartNumber="1",times=1, delay=0):
        start = identifier
        times = int(times)
        delay = float(delay)
        for i in range (times):
            if(start!=identifier):
                return
            playsound('sounds//fart-0'+str(fartNumber)+'.mp3')
            time.sleep(delay)
    def randomfarts(seed=random.randint(3,5), times=1, delay=0):
        seed = int(seed)
        times = int(times)
        delay = float(delay)
        start = identifier
        random.seed(seed)
        for i in range(times):
            fartChoice = random.randint(1,5)
            print("random fart:",fartChoice)
            if(start!=identifier):
                return
            playsound('sounds//fart-0'+str(fartChoice)+'.mp3')
            time.sleep(delay)
    def cyclefart(fartChoice=0, times=1, delay=0):
        fartChoice = int(fartChoice)
        times = int(times)
        delay = float(delay)
        start = identifier
        for i in range(times):
            fartChoice = fartChoice+1
            if(fartChoice>5):
                fartChoice=1
            print("cyclefart:",fartChoice)
            if(start!=identifier):
                return
            playsound('sounds//fart-0'+str(fartChoice)+'.mp3')
            time.sleep(delay)
    def playsound(sound):
        playsound('sounds//'+sound+'.mp3')
    def reset():
        global identifier
        identifier=identifier+1
        print("All is reset:",identifier)
    def screenglitch(pixelsChanged=5000, delay=10):
        start = identifier
        pixelsChanged = int(pixelsChanged)
        delay = float(delay)
        dc = win32gui.GetDC(0)
        for i in range(pixelsChanged):
            if(start!=identifier):
                return
            x=random.randint(0,win32api.GetSystemMetrics(0)-1)
            y=random.randint(0,win32api.GetSystemMetrics(1)-1)
            r,g,b = random.randint(1,255),random.randint(1,255),random.randint(1,255)
            color = win32api.RGB(r,g,b)
            win32gui.SetPixel(dc, int(x), int(y), color)
            time.sleep(delay/1000)

