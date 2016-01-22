# RasberryPi
Web Sockets and sensors, for linux/Pi!

Directions:

Start PiGPIO daemon with ```sudo pigpiod```

```
Pin 1: 3v3------|-------|--3v3 source
               5kR      |
Pin 2:  --------|-------|--GPIO 22
                        |
Pin 3:  X               |
                        |
pin 4:  GND  -----------|--GND
```
```python dht22_read.py```

Websocket dependencies:
```
sudo pip install tornado
sudo pip install websocket-client
```
