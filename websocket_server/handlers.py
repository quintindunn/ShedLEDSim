import json
import logging

from aiohttp.http_websocket import WSMessage

from structures import Client, LEDStrip

logger = logging.getLogger("handlers.py")


def echo_handler(msg: WSMessage):
    """
    Echos the message sent.
    :param msg: WSMessage sent from client.
    :return:
    """
    data = json.loads(msg.data)
    logger.info(f"Echo: `{data['content']}`")
    return {
        "type": "echo",
        "content": data['content']
    }


def setup_led_count_handler(msg: WSMessage, client: Client):
    """
    Initializes a new LEDStrip in the client.
    :param msg: Message sent from client.
    :param client: Client object.
    :return:
    """
    data = json.loads(msg.data)

    count = data['content']
    client.led_strip = LEDStrip(count)

    logger.info(f"Initialized LEDStrip with {count} LEDs to client {client.uuid}.")

    return {
        "type": "led-strip-initialized",
        "content": f"200,{count}"
    }
