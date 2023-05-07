import Adafruit_DHT
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class Sensor:
    def __init__(self):
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = 4
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.font = ImageFont.load_default()

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return temperature, humidity

    def display_on_oled(self, temperature, humidity):
        if temperature is None or humidity is None:
            return

        self.oled.fill(0)
        image = Image.new('1', (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        text = f'T: {temperature:.1f} C\nH: {humidity:.1f} %'
        draw.text((0, 0), text, font=self.font, fill=255)
        self.oled.image(image)
        self.oled.show()

