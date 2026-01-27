import frida
import sys
from datetime import datetime


def on_message(message, data):
    if message['type'] == 'send':
        print(f"\n[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Геоданные:")
        for key, value in message['payload'].items():
            print(f"  {key}: {value}")
    elif message['type'] == 'error':
        print(f"[ERROR] {message['description']}")


def main():
    try:
        device = frida.get_usb_device()

        try:
            session = device.attach("example_app")
            print("Подключено к процессу")
        except frida.ProcessNotFoundError:
            print("Процесс не найден, запускаем...")
            pid = device.spawn(["example_app"])
            session = device.attach(pid)
            device.resume(pid)
            print("Приложение запущено")

        with open("location_logger.js", "r", encoding="utf-8") as f:
            js_code = f.read()

        script = session.create_script(js_code)
        script.on("message", on_message)
        script.load()
        print("Скрипт активен. Ожидаем данные геолокации...")
        print("Нажмите Ctrl+C для остановки")

        sys.stdin.read()

    except KeyboardInterrupt:
        print("\nОстановлено пользователем")
    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        if 'session' in locals():
            session.detach()
        print("Скрипт остановлен")


if __name__ == "__main__":
    main()