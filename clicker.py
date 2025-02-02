import keyboard
import time
import pyautogui
from threading import Timer, Thread, Event, Lock
from datetime import datetime
from termcolor import colored
from tabulate import tabulate
import start_cookie_cliker
import os
import platform

print('👑 Кликер 1.0.0 👑')

isClicking = False
click_count = 0
global_datetime = datetime.now()
click_x, click_y = 0, 0
stop_event = Event()
click_lock = Lock()
info_interval = 10  # Default info interval (seconds)
click_interval = 0.1 # Default click interval (seconds)

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
            time.sleep(click_interval)
        except pyautogui.FailSafeException:
            print("Fail-safe triggered. Move your mouse.")
            stop_event.set()
            isClicking = False
        except Exception as e:
            print(f"An error occurred: {e}")
            stop_event.set()
            isClicking = False


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

def get_click_coordinates():
    if isClicking:
        return

    global click_x, click_y
    print("Наведите курсор на место клика и нажмите Enter...")
    input()
    click_x, click_y = pyautogui.position()
    print(f"Координаты клика: x={click_x}, y={click_y}")
    print("\n")
    print(f"Что бы запустить кликер нажмите: {colored("'ctrl' + 'alt' + '='", 'green')}")

keyboard.add_hotkey('ctrl+alt+-', get_click_coordinates)

def get_settings():
    global info_interval, click_interval
    print("Настройка параметров...")
    time.sleep(5)
    clear_console()
    while True:
        try:
            interval_str = input("Введите интервал обновления информации (секунды, Enter для 10): ")
            info_interval = int(interval_str) if interval_str else 10
            break
        except ValueError:
            print("Некорректный ввод. Попробуйте ещё раз.")
        except KeyboardInterrupt:
            print("Настройка параметров прервана.")
            return

    time.sleep(0.5)

    while True:
        try:
            interval_str = input("Введите интервал между кликами (секунды, Enter для 0.1): ")
            click_interval = float(interval_str) if interval_str else 0.1
            break
        except ValueError:
            print("Некорректный ввод. Попробуйте ещё раз.")
        except KeyboardInterrupt:
            print("Настройка параметров прервана.")
            return
    print("Настройка завершена.")
    clear_console()

def clear_console():
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    elif system in ["Linux", "Darwin"]: # Darwin - macOS
        os.system('clear')
    else:
        print("Неизвестная операционная система. Очистка консоли невозможна.")


if __name__ == "__main__":
    answer = input("Нужно ли запустить Cookie Clicker? (yes/no): ").lower()
    if answer == "yes":
        start_cookie_cliker.start_cookie_cliker()

    get_settings()
    get_click_coordinates()
    repeater(info_interval, info)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nКликер остановлен.")