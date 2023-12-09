import logging
import sys

import json

import aiohttp
from aiohttp import web
from aiohttp.http_websocket import WSMessage


logger = logging.getLogger(__name__)


def message_handler(msg: WSMessage) -> dict:
    data = json.loads(msg.data)

    match data['type']:
        case "echo":
            logger.info(f"Echo: `{data['content']}`")
            return {
                "type": "echo",
                "content": data['content']
            }


async def websocket_handler(request):
    """
    Handles new websocket connections.
    """

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    logging.info(f"New client.")

    # Send connection confirmed message.
    await ws.send_str(json.dumps({
        "type": "connection_confirmed",
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

                response = message_handler(msg)
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
