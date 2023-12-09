import random

from structures import LEDStrip


class Random:
    def __init__(self, led_strip: LEDStrip):
        self.led_strip = led_strip

    def random(self):
        for led in self.led_strip.leds:
            led.red = random.randint(0, 255)
            led.green = random.randint(0, 255)
            led.blue = random.randint(0, 255)


MODES = {
    "random": Random,
}
