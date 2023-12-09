import json
import logging

from aiohttp.http_websocket import WSMessage

logger = logging.getLogger("handlers.py")


def echo_handler(msg: WSMessage):
    data = json.loads(msg.data)
    logger.info(f"Echo: `{data['content']}`")
    return {
        "type": "echo",
        "content": data['content']
    }
