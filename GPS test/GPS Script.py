import socket
import time
from datetime import datetime

def calculate_checksum(nmea):
    checksum = 0
    for char in nmea[1:]:
        checksum ^= ord(char)
    return f"{checksum:02X}"

port = 5554
host = "localhost"
token = "token"

gpgga_template = "$GPGGA,{time},59.9253,N,30.3267,E,1,03,0.9,545.4,M,46.9,M,,"

try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((host, port))
    print("Соединение установлено с эмулятором GNSS")

    welcome = tcp.recv(1024).decode('ascii').strip()
    print(f"{welcome}")

    tcp.send(f"auth {token}\r\n".encode('ascii'))
    auth_response = tcp.recv(1024).decode('ascii').strip()
    print(f"{auth_response}")

    while True:
        current_time = datetime.utcnow().strftime("%H%M%S")

        nmea_gpgga_raw = gpgga_template.format(time=current_time)
        nmea_gpgga = f"{nmea_gpgga_raw}*{calculate_checksum(nmea_gpgga_raw)}"

        tcp.send(f"geo nmea {nmea_gpgga}\r\n".encode('ascii'))

        time.sleep(0.0001)

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    tcp.close()
    print("Соединение закрыто")