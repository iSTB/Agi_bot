import XBee_Threaded
from time import sleep
import sys
if __name__ == "__main__":
    xbee = XBee_Threaded.XBee("/dev/ttyUSB0")  # Your serial port name here

    # A simple string message
    sampledata=[]
    while True:
        try:
            sent = xbee.SendStr("0")
            Msg = xbee.Receive()
            if Msg:
                content = Msg
                print("Front: ",content[0],
                    " Right: ",content[2],
                    " left: ",content[4],
                    "rest: ", content[1],content[3],content[5])
                sampledata.append(content)
            sleep(0.5)
        except KeyboardInterrupt:
            break   
    import pickle

    f = open("behaviour_nothing.pickle","wb")
    pickle.dump(sampledata,f)
    f.close()
    # A message that requires escaping
    xbee.shutdown()
