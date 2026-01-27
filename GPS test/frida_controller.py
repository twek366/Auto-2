import frida
import time
from enum import Enum


class LocationMode(Enum):
    GPS = "GPS"
    GSM = "GSM"
    DISABLED = "DISABLED"


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
            session = device.attach("example_app")
            print("Подключено к запущенному процессу")
        except frida.ProcessNotFoundError:
            pid = device.spawn(["example_app"])
            session = device.attach(pid)
            device.resume(pid)
            time.sleep(1)
            print("Процесс успешно запущен")

        with open("location_manager.js", "r", encoding="utf-8") as f:
            script = session.create_script(f.read())

        script.on("message", on_message)
        script.load()
        print("Скрипт успешно загружен")

        def update_coords(lat, lng):
            try:
                script.exports_sync.setcoordinates(lat, lng)
                print("Координаты обновлены")
            except Exception as e:
                print(f"Ошибка обновления координат: {str(e)}")

        def update_mode(mode):
            try:
                script.exports_sync.setmode(mode.value)
                print(f"Режим обновлен: {mode.name}")
            except Exception as e:
                print(f"Ошибка обновления режима: {str(e)}")

        def update_accuracy(accuracy):
            try:
                script.exports_sync.setaccuracy(accuracy)
                print(f"Точность обновлена: {accuracy} м")
            except Exception as e:
                print(f"Ошибка обновления точности: {str(e)}")

        print("""\nКоманды:
  gps       - Режим высокой точности
  gsm       - Режим сети
  off       - Отключить геолокацию
  set lat,lng - Установить координаты
  acc метры - Установить точность
  exit      - Выход\n""")

        while True:
            cmd = input("> ").strip().lower()

            if cmd == "exit":
                break

            elif cmd == "gps":
                update_mode(LocationMode.GPS)
                update_accuracy(5.0)

            elif cmd == "gsm":
                update_mode(LocationMode.GSM)
                update_accuracy(500.0)

            elif cmd == "off":
                update_mode(LocationMode.DISABLED)

            elif cmd.startswith("set "):
                try:
                    parts = cmd[4:].replace(" ", "").split(",")
                    lat, lng = map(float, parts)
                    update_coords(lat, lng)
                except:
                    print("Неверный формат. Используйте: set 59.934280,30.335099")

            elif cmd.startswith("acc "):
                try:
                    accuracy = float(cmd[4:])
                    update_accuracy(accuracy)
                except:
                    print("Укажите числовое значение точности (acc 150)")

            else:
                print("Неизвестная команда")

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        if 'session' in locals():
            session.detach()
        print("Работа завершена")


if __name__ == "__main__":
    main()