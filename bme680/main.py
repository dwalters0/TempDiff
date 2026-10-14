# web server stuff
import network
import time
import socket
import json
# bme680 stuff
from bme680 import BME680
from machine import I2C, Pin

# Wi-Fi credentials
ssid = '<ADD wifi>'
password = '<Add wifi>'


def return_680_data():
    mypinout = I2C(0, scl=Pin(21), sda=Pin(20))
    sensor = BME680(mypinout, 10)
    data = {
        "temperature": round(sensor.readTemperature(), 2),
        "pressure": round(sensor.readPressure(), 2),
        "humidity": round(sensor.readHumidity(), 2),
        "air_resistance": round(sensor.readGas(), 2)
    }
    return json.dumps(data)


# Connect to network
def connect_wifi(ssid, password):
    # Connect to your network
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    # Wait for connection
    timeout = 10
    while not station.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if station.isconnected():
        print('Connection successful')
        print(station.ifconfig())
        return True
    else:
        print('Connection failed. Timeout reached')
        return False


def run_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    server.listen(1)

    print("Listening on", addr)

    while True:
        client, client_addr = server.accept()

        try:
            request = client.recv(1024)
            request_text = request.decode()

            print("Request from:", client_addr)
            print(request_text)

            body = return_680_data()

            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    + body
            )

            client.send(response.encode())

        except Exception as e:
            print("Error:", e)

        finally:
            client.close()


connect_wifi(ssid, password)
run_server()
