### What is this
This project uses a bme680 sensor and esp32 to record the temp and humidity indoors.
It also queries the open-meteo weather API for the outdoor temp and humidity.
Then it saves them to a sqlite db so that you can graph them to compare over time.

### the hardware
- Pimoroni BME680 Breakout Sensor [here](https://core-electronics.com.au/bme680-breakout-air-quality-temperature-pressure-humidity-sensor.html)
- ESP32-C3 Mini Dev Board (With Headers) [here](https://core-electronics.com.au/esp32-c3-mini-dev-board-risc-v-processor-wi-fi-bt5-smd-compatible.html)
- PiicoDev Protoboard [here](https://core-electronics.com.au/piicodev-protoboard.html)

### the software
- The main.py file runs the logging of the temperatures and saves to database.db in the same directory. The URL for the query to the sensor device needs to be set, as well as the lat and lon for the open-meteo query. 
- The dockerfile can build it as a container and deploy.sh will build and run it.
- Inside the bme680 folder is a main.py file, that along with the included Soldered-BME680-MicroPython-Library library are uploaded to the esp32 using Thonny. It's micropython that the esp32 can run. The esp32 simply runs main.py on boot once it has been flashed with micropython by Thonny. The wifi credentials and pin IDs will or may differ.
