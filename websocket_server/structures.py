import uuid

from aiohttp.web_request import Request


class Client:
    def __init__(self, request: Request):
        self.request = request
        self.led_strip: LEDStrip | None = None
        self.uuid = str(uuid.uuid4())


class LEDStrip:
    def __init__(self, led_count: int):
        self.leds = [LED(0, 0, 0) for _ in range(led_count)]


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
