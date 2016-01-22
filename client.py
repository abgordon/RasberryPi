from PIL import Image
import websocket
import cStringIO
import base64
import time
import logging

logging.basicConfig()

TAF = True

class WSClient():
 
    def __init__(self):
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:8888/ws",
        on_message = self.on_message,
        on_error = self.on_error,
        on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
 
        # self.ws.send(u"Hello, world!".encode('utf8'))
        self.ws.send("Huggaw, world!")

    def on_message(self, ws, message):
        print "got me a message:", message, ws
 
    def on_error(self, ws, error):
        print error
 
    def on_close(self, ws):
        print "connection closed"
 
    def on_open(self, ws):
        print "connected"

        while TAF:
            time.sleep(1)
            self.ws.send("Huggaw, world!")

 
if __name__ == "__main__":
    client = WSClient()