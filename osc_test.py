import argparse
import random
import time
import triad_openvr

from pythonosc import osc_message_builder
from pythonosc import udp_client


v = triad_openvr.triad_openvr()
v.print_discovered_objects()
client = udp_client.SimpleUDPClient("192.168.2.5", 3333)

while(True):
  data =  v.devices["tracker_1"].get_pose_quaternion_for_unity()

  client.send_message("/tx", data[0])
  client.send_message("/ty", data[1])
  client.send_message("/tz", data[2])
  
  client.send_message("/rx", data[3])
  client.send_message("/ry", data[4])
  client.send_message("/rz", data[5])
  
  #print("tx " + "%.4f" % data[0], end=", ")
  #print("ty " + "%.4f" % data[1], end=", ")
  #print("tz " + "%.4f" % data[2], end=", ")
  #print("rx " + "%.4f" % data[3], end=", ")
  #print("ry " + "%.4f" % data[4], end=", ")
  #print("rz " + "%.4f" % data[5], end="\n")

  time.sleep(1.0/120.0)
