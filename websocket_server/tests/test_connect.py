import json
import time
import uuid
from unittest import TestCase

import websocket


class TestConnection(TestCase):
    def test_connect(self):
        """
        Connects to the websocket, sends an echo message, checks they're equivalent.
        :return:
        """

        # Connect to the websocket.
        ws = websocket.WebSocket(debug=True)
        ws.connect("ws://127.0.0.1:9090")

        # Generate the message
        msg = f"Test {str(uuid.uuid4())}"

        # Generate the packet to send.
        send = json.dumps({
            "type": "echo",
            "content": msg
        })

        ws.send(send)

        # Check the response is equal to the data sent.
        recv = ws.recv()
        self.assertEqual(recv, send)
