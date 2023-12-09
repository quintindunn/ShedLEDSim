import json
from unittest import TestCase

import websocket


class TestLed(TestCase):
    def test_initialize(self):
        led_count = 300

        # Connect to the websocket.
        ws = websocket.WebSocket(debug=True)
        ws.connect("ws://127.0.0.1:9090")

        ws.recv()

        ws.send(json.dumps({
            "type": "setup-led-count",
            "content": led_count
        }))

        response = json.loads(ws.recv())

        self.assertEqual(response['type'], "led-strip-initialized")
        self.assertEqual(response['content'], f"200,{led_count}")
