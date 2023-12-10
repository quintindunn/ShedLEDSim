import random

import typing

if typing.TYPE_CHECKING:
    from structures import LEDStrip


class BaseMode:
    def __init__(self, led_strip: "LEDStrip"):
        self.led_strip = led_strip

    def update(self):
        pass


class Random(BaseMode):
    def __init__(self, led_strip: "LEDStrip"):
        super().__init__(led_strip)

    def update(self):
        for led in self.led_strip.leds:
            led.red = random.randint(0, 255)
            led.green = random.randint(0, 255)
            led.blue = random.randint(0, 255)


MODES = {
    "random": Random,
}
