import uuid

from aiohttp.web_request import Request

from modes import BaseMode


class Client:
    def __init__(self, request: Request):
        self.request = request
        self.led_strip: LEDStrip | None = None
        self.uuid = str(uuid.uuid4())
        self.led_mode: BaseMode | None = None


class LEDStrip:
    def __init__(self, led_count: int):
        self.leds = [LED(0, 0, 0) for _ in range(led_count)]

    def __str__(self):
        return str(self.leds)


class LED:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def r(self):
        return self.red

    @property
    def g(self):
        return self.green

    @property
    def b(self):
        return self.blue

    def __str__(self):
        return f"[{self.red},{self.green},{self.blue}]"

    __repr__ = __str__
