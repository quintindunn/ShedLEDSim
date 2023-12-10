import logging
import sys

import json

import aiohttp
from aiohttp import web
from aiohttp.http_websocket import WSMessage

from handlers import echo_handler, setup_led_count_handler, dump_led_handler, update_mode_handler, \
    update_display_handler

from structures import Client

logger = logging.getLogger(__name__)

clients = []


def message_handler(msg: WSMessage, client: Client) -> dict:
    data = json.loads(msg.data)

    match data['type']:
        case "echo":
            return echo_handler(msg=msg)
        case "setup-led-count":
            return setup_led_count_handler(msg=msg, client=client)
        case "dump-leds":
            return dump_led_handler(client=client)
        case "update-mode":
            return update_mode_handler(msg=msg, client=client)
        case "update-display":
            return update_display_handler(client=client)


async def websocket_handler(request):
    """
    Handles new websocket connections.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    client = Client(request)
    clients.append(client)

    logging.info(f"New client.")

    # Send connection confirmed message.
    await ws.send_str(json.dumps({
        "type": "connection-confirmed",
        "content": "Connection confirmed!"
    }))

    # While the socket is alive, listen for messages.
    async for msg in ws:
        # Type-hinting for development.
        msg: WSMessage

        # Make sure the message is text, not an error.
        if msg.type == aiohttp.WSMsgType.TEXT:
            # Check if the packet was to close the connection.
            if msg.data == 'close':
                await ws.close()
            else:
                # Generate a response packet.

                response = message_handler(msg=msg, client=client)
                if response:
                    await ws.send_str(json.dumps(response))
                else:
                    logger.warning(f"No known response for message, {msg.data[:1000]}")

        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.warning(f'Websocket connection closed with exception {ws.exception()}')

    logger.info('Websocket connection closed')
    return ws


def run(host: str = "127.0.0.1", port: int = 9090):
    app = web.Application()
    app.add_routes([web.get("/", websocket_handler)])

    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    import argparse
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    args = argparse.ArgumentParser()

    args.add_argument("-H", default="127.0.0.1", type=str, help="Host IP address.")
    args.add_argument("-P", default=9090, type=int, help="Port.")

    args = args.parse_args()

    run(host=args.H, port=args.P)
