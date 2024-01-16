import asyncio
from websockets.server import serve

from websockets.sync.client import connect

def hello():
    with connect("ws://52.ddnsking.com/ws/chat/0/?token=300459c4def815261982d6f9f85ab7bbfb9b8dbd") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()