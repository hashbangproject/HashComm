from communication import HashComm
import struct
from time import sleep, clock

def confirm(comm):
    try: 
        c = clock()
        msgType, _ = comm.getMessage()
        nc = clock()
        print(nc - c)
        if msgType != 0x00: print("Got bad confirmation. %i" % msgType)
    except:
        print("timeout")

def main():
    comm = HashComm('COM14')

    # Send a ping and get a response
    #comm.putMessage(0x01, 0x01, b'')
    #msgType, _ = comm.getMessage()
    #if msgType != 0x00: print("Got bad ping. %i" % msgType)
    #else: print("Communication initialized.")

    msg1 = struct.pack('<fff', 0, 20, 0)
    msg2 = struct.pack('<fff', 0, 0, 0)
    print("Press key to send message...")
    while True:
        if 'q' in input(): break
        comm.putMessage(0x04, 0x01, msg1)
        confirm(comm)
        if 'q' in input(): break
        comm.putMessage(0x04, 0x01, msg2)
        confirm(comm)

if __name__ == '__main__':
    main()
