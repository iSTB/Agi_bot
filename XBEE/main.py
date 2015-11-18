import XBee
from time import sleep

if __name__ == "__main__":
    xbee = XBee.XBee("/dev/ttyUSB1")  # Your serial port name here

    # A simple string message
    sent = xbee.SendStr("A")
    sleep(0.25)
    Msg = xbee.Receive()
    if Msg:
        content = Msg.decode('ascii')
        print("Msg: " + content)

    # A message that requires escaping
    sent = xbee.SendStr("A")
    sleep(0.25)
    Msg = xbee.Receive()
    if Msg:
        content = Msg.decode('ascii')
        print("Msg: " + content)
