#!/usr/bin/env python3

import fcntl
import array
import os
import struct
import select
import threading
import subprocess
import decode
import logging

logger = logging.getLogger()

LIRC_GET_REC_MODE = 0x80046902 # _IOR('i', 0x00000002, __u32)
LIRC_GET_LENGTH = 0x8004690F # _IOR('i', 0x0000000f, __u32)
LIRC_MODE_MODE2 = 0x00000004
PULSE_BIT = 0x01000000
PULSE_MASK = 0x00FFFFFF

result = array.array("I", [0])
lirc_t = "i"
dataSequenceThread = []

def readLine(fd, interval):
  data = []
  #print( "entering read()" )
  # wait for up to <interval> milliseconds
  readable,_,_ = select.select([fd],[],[], interval)
  #print( "after select")
  if fd in readable:
    rawbuf = os.read(fd, struct.calcsize(lirc_t))
    #print("read")
    rawvalue, = struct.unpack(lirc_t, rawbuf)
    pulseflag = rawvalue & PULSE_BIT
    duration = rawvalue & PULSE_MASK
  #print( rawvalue)
  #print( pulseflag )
  #print( duration )
    if pulseflag != 0:
      #dataDict = {"pulse": str(duration) }
      data.append("pulse")
      data.append(duration)
    else:
      data.append("space")
      data.append(duration)
      #dataDict = {"space": str(duration) }

  return data

def readSequence(fd, interval):
  dataSequence = []
  isReceiving = True
  while isReceiving:
    dataDict = readLine(fd, interval)
    #print( data )
    if len(dataDict) == 0:
      isReceiving = False
    else:
      dataSequence.append(dataDict)

  return dataSequence
  
def readSequenceThread(fd, interval):
  global dataSequenceThread
  
  dataSequenceThread = readSequence( fd, interval )
  

def openDevice( devicePath ):
  #print( "opening device" )
  fd = os.open(devicePath, os.O_RDONLY)
  #print( "...opened" )
  if fcntl.ioctl(fd, LIRC_GET_REC_MODE, result, True) == -1:
    raise IOError("cannot use {!r} as a raw LIRC device. Is it a LIRC device?".format(self.device))
  if result[0] != LIRC_MODE_MODE2:
    raise IOError("cannot use {!r} as a raw LIRC device. Is it a raw (!) LIRC device?".format(self.device))
   
  return fd
    


        
def irsend(deviceName, keyName):    
  logger.debug(keyName)
  deviceConfig = decode.readConf()
  global dataSequenceThread
  isMatch = True
  
  fd = openDevice( "/dev/lirc1" )
  if ( fd ):
    # read all of the characters waiting in the buffer 
    #dataSequence = readSequence( fd, -1.5 )
    
    # start the receiving thread
    x = threading.Thread(target=readSequenceThread, args=(fd, 0.200,))
    x.start()
        
    # push the "button"
    #command = ["irsend", "SEND_ONCE", deviceName, keyName]
    #subprocess.call( command )
    os.system("irsend SEND_ONCE %s %s" %(deviceName, keyName))

    # wait for the thread to finish reading the sequence
    x.join()
    
    print( "thread joined" )
    #print( dataSequenceThread )
    logger.debug(dataSequenceThread)
    keyReceived = decode.decode(dataSequenceThread, deviceName, deviceConfig)
    if keyReceived != keyName:
      isMatch = False
  return isMatch

##########################################################################
if __name__ == "__main__":
    main()
