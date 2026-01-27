import frida
import sys


def on_message(message, data):
    if message['type'] == 'send':
        print(message['payload'])
    else:
        print(f"Frida message: {message}")


def main():
    device = frida.get_usb_device()
    app_package = "example_app"  # Замените на ваш пакет!

    try:
        pid = device.spawn([app_package])
        session = device.attach(pid)
    except Exception as e:
        print(f"Error: {e}. Attaching to running app...")
        session = device.attach(app_package)

    with open("ssl_traffic_hook.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())

    script.on('message', on_message)
    script.load()

    try:
        device.resume(pid)
    except:
        pass

    print("Frida script loaded. Press Ctrl+C to stop.")
    sys.stdin.read()


if __name__ == "__main__":
    main()