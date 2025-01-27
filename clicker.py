import keyboard
import time
from threading import Timer
from datetime import datetime
from termcolor import colored
import pyautogui
# import start_cookie_cliker

# start_cookie_cliker.start_cookie_cliker()

print('👑 Кликер 1.0.0 👑')

isClicking = False
click_count = 0

global_datetime = datetime.now()

def repeater(interval, function):
    Timer(interval, repeater, [interval, function]).start()
    function()

def set_clicker():
  global isClicking
  if isClicking:
    isClicking = False
    print(colored('Кликер Отключёт', 'red', attrs=['underline']))
   
  else:
    isClicking = True
    print(colored('Кликер Включён', 'green', attrs=['underline']))

keyboard.add_hotkey('ctrl+alt+=', set_clicker)

def click():
  global click_count
  time.sleep(0.01)
  pyautogui.click(x=145, y=458)
  click_count = click_count + 1
  if isClicking == False:
    click_count = 0

def info():
  global global_datetime
  current_datetime = datetime.now()
  time_difference = current_datetime - global_datetime
  if isClicking:
    print('Игра запущена уже 🕙︎ →  ', colored(str(time_difference)[0:7], 'cyan'), ' сек.')
    print('💎 Кликов 💎 : ' ,colored(str(click_count), 'green', attrs=['underline', 'bold']))

repeater(10, info)

while True:
  if isClicking:
    click()