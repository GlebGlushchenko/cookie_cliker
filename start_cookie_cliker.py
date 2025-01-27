import os

def start_cookie_cliker():
    path = "C:\Program Files (x86)\Steam\steamapps\common\Cookie Clicker\Cookie Clicker.exe" #Или другой путь
    try:
        os.startfile(path)
        print("Cookie Clicker запущен.")
    except FileNotFoundError:
        print(f"Ошибка: файл {path} не найден. Проверьте путь.")
    except Exception as e:
        print(f"Ошибка при запуске Cookie Clicker: {e}")