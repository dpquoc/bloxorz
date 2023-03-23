import os
import subprocess
import pyautogui
import time
import pydirectinput
import keyboard
from PIL import Image


class AutoGUI:
    def __init__(self, img_path, delay=1):
        self.img_path = img_path
        self.delay = delay
        self.image = None
        try:
            self.image = Image.open(img_path)
        except:
            print(f"Failed to load image: {img_path}")

    def find_click(self):
        if self.image is not None:
            try:
                center = pyautogui.locateCenterOnScreen(
                    self.image, confidence=0.9)
                if center is not None:
                    pyautogui.click(center)
                    time.sleep(self.delay)
                    return True

            except:
                pass

        return False


def visual_output(actions, instage=False, passcode=None):
    newgame = AutoGUI('./img/newgame.png', 1)
    skip = AutoGUI('./img/skip.png', 1)
    loadstage = AutoGUI('./img/loadstage.png', 1)
    enterpasscode = AutoGUI('./img/enterpasscode.png', 1)

    while True:
        if not instage :
            if passcode==None:
                if newgame.find_click():
                    skip.find_click()
            else:          
                if loadstage.find_click():
                    if enterpasscode.find_click():
                        pyautogui.typewrite(passcode)
                        instage=True
                        time.sleep(6)
        else:
            if pyautogui.locateCenterOnScreen('./img/menu.png' , confidence=0.9) != None :
                for action in actions:
                    pydirectinput.press(action.lower())
                    time.sleep(0.3)
                print('Done')
                break



# visual_output(["DOWN","RIGHT","RIGHT","RIGHT","RIGHT","RIGHT","RIGHT","DOWN"], False ,"780464")
