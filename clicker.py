import keyboard
import time
import pyautogui
from threading import Timer, Thread, Event, Lock
from datetime import datetime
from termcolor import colored
from tabulate import tabulate

print('👑 Кликер 1.0.0 👑')

isClicking = False
click_count = 0
global_datetime = datetime.now()
click_x, click_y = 0, 0
stop_event = Event()
click_lock = Lock()

def repeater(interval, function):
    Timer(interval, repeater, [interval, function]).start()
    function()

def set_clicker():
    global isClicking, global_datetime, click_count
    if isClicking:
        isClicking = False
        stop_event.set()
        print(colored('Кликер Отключен', 'red', attrs=['underline']))
        global_datetime = datetime.now()
        click_count = 0
    else:
        isClicking = True
        stop_event.clear()
        global_datetime = datetime.now()
        click_thread = Thread(target=click)
        click_thread.daemon = True
        click_thread.start()
        print(colored('Кликер Включен', 'green', attrs=['underline']))

keyboard.add_hotkey('ctrl+alt+=', set_clicker)

def click():
    global click_count
    while not stop_event.is_set():
        try:
            pyautogui.click(x=click_x, y=click_y)
            with click_lock:
                click_count += 1
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Move your mouse.")
            stop_event.set()
        except Exception as e:
            print(f"An error occurred: {e}")
            stop_event.set()

def info():
    global global_datetime
    current_datetime = datetime.now()
    time_difference = current_datetime - global_datetime
    elapsed_seconds = time_difference.total_seconds()
    if isClicking and elapsed_seconds > 0:
        clicks_per_minute = (click_count / elapsed_seconds) * 60
        data = [
            ["Время работы", colored(str(time_difference)[0:7], 'cyan') + " сек."],
            ["Количество кликов", colored(str(click_count), 'green', attrs=['underline', 'bold'])],
            ["Кликов/мин", colored(f"{clicks_per_minute:.2f}", 'yellow')]
        ]
        print("\n")
        print(tabulate(data, headers=["Метрика", "Значение"], tablefmt="grid"))
        print("\n")
        print(f"Что бы приостановить кликер нажмите: {colored("'ctrl' + 'alt' + '='", 'green')}")

repeater(10, info)

def get_click_coordinates():
    if(isClicking):
        return
    
    global click_x, click_y
    print("Наведите курсор на место клика и нажмите Enter...")
    input()
    click_x, click_y = pyautogui.position()
    print(f"Координаты клика: x={click_x}, y={click_y}")
    print("\n")
    print(f"Что бы запустить кликер нажмите: {colored("'ctrl' + 'alt' + '='", 'green')}")

keyboard.add_hotkey('ctrl+alt+-', get_click_coordinates) # Добавлено

if __name__ == "__main__":
    get_click_coordinates()
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
        print("\nКликер остановлен.")