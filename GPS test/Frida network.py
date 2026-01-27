import frida
import time


def on_message(message, data):
    if message['type'] == 'send':
        print(f"{message['payload']}")
    else:
        print(f"[Frida] {message}")


def main():
    try:
        device = frida.get_usb_device()
        print(f"Подключено к устройству: {device.name}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return

    try:
        try:
            session = device.attach("example_app")  # Замените на пакет вашего приложения
            print("Подключено к запущенному процессу")
        except frida.ProcessNotFoundError:
            pid = device.spawn(["example_app"])  # Замените на пакет вашего приложения
            session = device.attach(pid)
            device.resume(pid)
            time.sleep(1)
            print("Процесс успешно запущен")

        with open("okhttp_interceptor.js", "r", encoding="utf-8") as f:
            script = session.create_script(f.read())

        script.on("message", on_message)
        script.load()
        print("Логи HTTP-запросов:")

        input("Нажмите Enter для выхода...\n")

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        if 'session' in locals():
            session.detach()
        print("Работа завершена")


if __name__ == "__main__":
    main()
