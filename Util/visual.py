import os
import subprocess
import pyautogui
import time
import pydirectinput


class AutoGUI:
    def __init__(self, img, delay=1):
        self.img = img
        self.delay = delay
        
    def find_click(self):
        center = None
        try:
            center = pyautogui.locateCenterOnScreen(self.img , confidence=0.9)
            pyautogui.click(center)
        except:
            pass
         
        if center == None: return False
        time.sleep(self.delay)
        return True
    
    
    
    
def open_game():
    url = 'https://www.coolmathgames.com/0-bloxorz'
    if os.name == 'nt': # Windows
        os.startfile(url)
    elif os.name == 'posix': # macOS or Linux
        opener = 'open' if os.uname().sysname == 'Darwin' else 'xdg-open'
        subprocess.Popen([opener, url])

def visual_output(actions, instage=False, passcode=None ): 
    newgame = AutoGUI('./img/newgame.png', 1)
    skip = AutoGUI('./img/skip.png', 1)
    loadstage = AutoGUI('./img/loadstage.png', 1)
    enterpasscode = AutoGUI('./img/enterpasscode.png', 1)
    
    while True:
        if not instage :
            if passcode==None:
                newgame.find_click()
                skip.find_click()
            else:          
                loadstage.find_click()
                if (enterpasscode.find_click()):
                    pyautogui.typewrite(passcode)
                    time.sleep(6)
            instage=True
                    
        if pyautogui.locateCenterOnScreen('./img/menu.png' , confidence=0.9) != None :      
            for action in actions:
                pydirectinput.press(action.lower())
                time.sleep(0.3)
            print('Done')
            break
        
visual_output(["DOWN","RIGHT","RIGHT","RIGHT","RIGHT","RIGHT","RIGHT","DOWN"],"780464")