from PIL import Image
import websocket
import cStringIO
import base64
import time
import logging

logging.basicConfig()

ip = "104.154.67.221"
port = "8080"

class WSClient():

    def __init__(self):
        websocket.enableTrace(False)
        print "Connecting to ws://" + ip + ":" + port +"..."
        self.ws = websocket.WebSocketApp("ws://" + ip + ":" + port,
        on_message = self.on_message,
        on_error = self.on_error,
        on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

        self.ws.send("Successfully connected.")

    def on_message(self, ws, message):
        print "rcvd:", message, ws

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "connection closed"

    def on_open(self, ws):
        print "connected"

        while True:
            time.sleep(1)
            self.ws.send("Test msg")


if __name__ == "__main__":
    client = WSClient()
