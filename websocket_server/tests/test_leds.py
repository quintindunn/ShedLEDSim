import json
from unittest import TestCase

import websocket


def initialize_ws_with_leds(test: TestCase, led_count: int):

    # Connect to the websocket.
    ws = websocket.WebSocket(debug=True)
    ws.connect("ws://127.0.0.1:9090")

    ws.recv()

    ws.send(json.dumps({
        "type": "setup-led-count",
        "content": led_count
    }))

    response = json.loads(ws.recv())

    test.assertEqual(response['type'], "led-strip-initialized")
    test.assertEqual(response['content'], f"200,{led_count}")

    return ws

class TestLed(TestCase):
    def test_initialize(self):
        led_count = 300

        initialize_ws_with_leds(self, led_count)

    def test_dump(self):
        led_count = 300

        ws = initialize_ws_with_leds(self, led_count)

        ws.send(json.dumps({
            "type": "dump-leds"
        }))

        correct_response = [[0, 0, 0] for _ in range(led_count)]

        response = json.loads(ws.recv())

        self.assertEqual(json.loads(response['content']), correct_response)
