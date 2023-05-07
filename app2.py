import os
import time
from flask import Flask, jsonify, send_from_directory, Response, render_template
from threading import Timer
from modules.sensor import Sensor
from modules.camera_controller import CameraController

# Initialize Flask app
app = Flask(__name__)
sensor = Sensor()
camera_controller = CameraController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    temperature, humidity = sensor.get_data()
    return jsonify({'temperature': temperature, 'humidity': humidity})

@app.route('/image/<filename>')
def image(filename):
    return send_from_directory(camera_controller.image_folder, filename)

@app.route('/capture')
def capture():
    filename = camera_controller.take_picture()
    temperature, humidity = sensor.get_data()
    sensor.display_on_oled(temperature, humidity)
    with open(filename, "rb") as img:
        return Response(img.read(), content_type="image/jpeg")

@app.route('/images')
def images():
    file_list = [f for f in os.listdir(camera_controller.image_folder) if f.endswith('.jpg')]
    return jsonify({'images': file_list})

def capture_and_display():
    while True:
        temperature, humidity = sensor.get_data()
        sensor.display_on_oled(temperature, humidity)

        # Check if an hour has passed since the last picture was taken
        current_time = time.time()
        if current_time - capture_and_display.last_capture_time >= 3600:
            # camera_controller.take_picture()
            capture_and_display.last_capture_time = current_time

        # Wait for 5 seconds
        time.sleep(5)

# Initialize last_capture_time as the script start time
capture_and_display.last_capture_time = time.time()

if __name__ == '__main__':
    Timer(0, capture_and_display).start()
    app.run(host='0.0.0.0', port=8080)

