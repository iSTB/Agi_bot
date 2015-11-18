import XBee_Threaded
from time import sleep

if __name__ == "__main__":
    xbee = XBee_Threaded.XBee("/dev/ttyUSB1")  # Your serial port name here

    # A simple string message
    sent = xbee.SendStr("0")
    Msg = xbee.Receive()
    if Msg:
        content = Msg.decode('ascii')
        print("Msg: " + content)

    # A message that requires escaping
    xbee.SendStr("0")
    Msg = xbee.Receive()
    if Msg:
        content = Msg.decode("ascii")
        print("Msg: " + content)

    xbee.shutdown()
