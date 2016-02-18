from PIL import Image
import websocket
import cStringIO
import base64
import time
import logging

logging.basicConfig()
ip = "104.197.37.118"
port = "8080"
endpoint = "echo"

class WSClient():

    def __init__(self):
        websocket.enableTrace(True)
        print "Connecting to ws://" + ip + ":" + port + "/" + endpoint + "..."
        self.ws = websocket.WebSocketApp("ws://" + ip + ":" + port + "/" + endpoint,
        on_message = self.on_message,
        on_error = self.on_error,
        on_close = self.on_close)
        self.ws.on_open = self.on_open
        print "successfully connected."
        self.ws.run_forever()


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
            msg = "test msg"
            print msg #see whats going out
            self.ws.send(msg)


if __name__ == "__main__":
    client = WSClient()
