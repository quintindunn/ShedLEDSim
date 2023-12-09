import json
import logging

from aiohttp.http_websocket import WSMessage

from structures import Client, LEDStrip
from modes import MODES

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


def dump_led_handler(client: Client):
    """
    Returns an Array of the LEDs
    :param client: Client object.
    :return:
    """

    logger.debug(f"Dumping LEDs to client {client.uuid}")

    return {
        "type": "led-dump",
        "content": f"{str(client.led_strip)}"
    }


def update_mode_handler(msg: WSMessage, client: Client):
    """
    Updates the LED mode the client is using.
    :param msg: Message sent from client.
    :param client: Client object.
    :return:
    """

    data = json.loads(msg.data)

    client_mode = data['content']
    logger.info(f"Setting client {client.uuid} mode to {client_mode}")

    for mode, mode_class in MODES.items():
        if client_mode == mode:
            client.led_mode = mode_class(client.led_strip)
            client.led_mode.random()
            break
    else:
        client_mode = "MODE_UPDATE_FAILURE"

    return {
        "type": "mode-update",
        "content": client_mode
    }