from bme680 import BME680
from machine import I2C, Pin

mypinout = I2C(0, scl=Pin(21), sda=Pin(20))
sensor = BME680(mypinout,10)
print("Temperature: " + str(sensor.readTemperature()) +"°C")
print("Air pressure: " + str(sensor.readPressure()) + "hPa")
print("Relative Humidity: " + str(sensor.readHumidity()) + "%")
print("Air resistance: " + str(sensor.readGas()) + "MΩ")