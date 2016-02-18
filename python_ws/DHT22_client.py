#!/usr/bin/env python
import websocket
import cStringIO
import time
import logging
import time
import atexit
import pigpio
import DHT22

logging.basicConfig()
ip = "104.197.37.118"
port = "8080"
endpoint = "echo"


#Simple web socket class
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
        # Intervals of about 2 seconds or less will eventually hang the DHT22.
        INTERVAL=3


        r = 0

        next_reading = time.time()

        while True:

          r += 1

          s.trigger()

          time.sleep(0.2)

          print("{} {} {} {:3.2f} {} {} {} {}".format(r, s.humidity(), s.temperature(), s.staleness(),s.bad_checksum(), s.short_message(), s.missing_message(),s.sensor_resets()))

          next_reading += INTERVAL

          time.sleep(next_reading-time.time()) # Overall INTERVAL second polling.

        s.cancel()

        pi.stop()



if __name__ == "__main__":
    pi = pigpio.pi()
    s = DHT22.sensor(pi, 22, LED=16, power=8)
    client = WSClient()
