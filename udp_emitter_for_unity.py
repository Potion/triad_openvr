import triad_openvr
import time
import sys
import struct
import socket
import argparse
from pynput.keyboard import Key, Listener

parser = argparse.ArgumentParser()
parser.add_argument('--port', '-p', help= "UDP port", type = int, default= 8051)
parser.add_argument('--tracker', '-t', help= "Tracker ID", type = str, default= 'tracker_1')
parser.add_argument('--seconds', '-s', help= "Predicted Seconds to Photons from Now", type = float, default= 0.08)
args = parser.parse_args()

predictedSecondsToPhotonsFromNow = args.seconds
interval = 1.0/250.0
trackerID = args.tracker

def on_press(key):
    global predictedSecondsToPhotonsFromNow

    try:
        print('{0} pressed'.format(key))  
        if key == Key.up:
            print('UP pressed')
            predictedSecondsToPhotonsFromNow += 0.01
        elif key == Key.down:
            predictedSecondsToPhotonsFromNow -= 0.01

        print('predicting pose at {0} seconds from now'.format(predictedSecondsToPhotonsFromNow))

    except Exception as inst :
        print(inst)
                    

# listen to keyboard events
listener = Listener(on_press=on_press)
listener.start()

# connect udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', args.port)

v = triad_openvr.triad_openvr()
v.print_discovered_objects()
    
if interval:
    while(True):        
        start = time.time()
        txt = ""
        data =  v.devices[trackerID].get_pose_quaternion_for_unity_with_prediction(predictedSecondsToPhotonsFromNow)
        sent = sock.sendto(struct.pack('d'*len(data), *data), server_address)        
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
