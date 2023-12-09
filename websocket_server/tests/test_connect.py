import json
import time
import uuid
from unittest import TestCase

import websocket


class TestConnection(TestCase):
    def test_connect(self):
        msg = f"Test {str(uuid.uuid4())}"

        ws = websocket.WebSocket(debug=True)
        ws.connect("ws://127.0.0.1:9090")

        send = json.dumps({
            "type": "echo",
            "content": msg
        })

        ws.send(send)
        recv = ws.recv()

        self.assertEqual(recv, send)
