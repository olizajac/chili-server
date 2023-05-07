import time
import Adafruit_DHT
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from flask import Flask, jsonify, send_from_directory, Response
import os
from picamera import PiCamera
from threading import Timer

# Initialize DHT22 sensor and OLED display
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
font = ImageFont.load_default()

# Initialize Flask app
app = Flask(__name__)
camera = PiCamera()
image_folder = "images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Get sensor data
def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

# Take a picture and save it
def take_picture(filename):
    camera.capture(filename)

# Display data on the OLED
def display_on_oled(temperature, humidity):
    if temperature is None or humidity is None:
        return

    oled.fill(0)
    image = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    text = f'T: {temperature:.1f} C\nH: {humidity:.1f} %'
    draw.text((0, 0), text, font=font, fill=255)
    oled.image(image)
    oled.show()

@app.route('/data')
def data():
    temperature, humidity = get_sensor_data()
    return jsonify({'temperature': temperature, 'humidity': humidity})

@app.route('/image/<filename>')
def image(filename):
    return send_from_directory(image_folder, filename)

@app.route('/capture')
def capture():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{image_folder}/{timestamp}.jpg"
    take_picture(filename)
    temperature, humidity = get_sensor_data()
    display_on_oled(temperature, humidity)
    with open(filename, "rb") as img:
        return Response(img.read(), content_type="image/jpeg")

def capture_and_display():
    while True:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{image_folder}/{timestamp}.jpg"
        take_picture(filename)
        temperature, humidity = get_sensor_data()
        display_on_oled(temperature, humidity)

        # Wait for an hour
        time.sleep(3600)

if __name__ == '__main__':
    Timer(0, capture_and_display).start()
    app.run(host='0.0.0.0', port=8080)

