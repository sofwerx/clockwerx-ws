#!/usr/bin/env python3
import fcntl
import array
import os
import struct
import select
import threading
import subprocess
import logging

logger = logging.getLogger()

PERCENT = 0.35
BITS = 0
ZERO_PULSE = -1
ZERO_SPACE = -1
ONE_PULSE = -1
ONE_SPACE = -1
PRE_DATA = 0x33B8
PRE_DATA_BITS = 0
HEADER_PULSE = -1
HEADER_SPACE = -1

bitTotal = 0
header_pulse_upper = 0
header_pulse_lower = 0
header_space_upper = 0
header_space_lower = 0

zero_pulse_upper = 0
zero_pulse_lower = 0
zero_space_upper = 0
zero_space_lower = 0

one_pulse_upper = 0
one_pulse_lower = 0
one_space_upper = 0
one_space_lower = 0

#get all *.conf files
def getConfFiles():
  allConfFiles = []
  files = os.listdir("/etc/lirc")
  for file in files:
        if file.endswith('.conf'):
            allConfFiles.append(file)
  return allConfFiles

#format file contents
def formatConfFiles(file):
  contents = []
  temp = []
  for currentLine in file:
    if currentLine.startswith("#"):
      continue
    else:
      temp.append("".join(currentLine.strip()))
  file.close()

  for line in temp:
    new_format = line.replace('\t', ' ')
    contents.append(' '.join(new_format.split()))
  while '' in contents:
    contents.remove('')
  contents = [x.split(" ") for x in contents]
  return contents

#parse the config files
def parseConfFile(allDevices, contents):
  index1 = -1
  index2 = -1
  name = "" 
  pre_data = ""
  for i in range(len(contents)):
      for j in range(len(contents[i])):
        if contents[i][j] == 'begin' and contents[i][j+1] == 'remote':
          index1 = i
        if contents[i][j] == 'name':
          name = contents[i][j+1]
          j=j+1
        if contents[i][j] == 'pre_data':
          pre_data = contents[i][j+1][2:]
          j=j+1
        if contents[i][j] == 'begin' and contents[i][j+1] == 'codes':
          for k in range(i+1,len(contents)):
            if contents[k][0] == 'end' and contents[k][1] == 'codes':
              i = k+1
              break
            tempVal = contents[k][1][2:]
            contents[k][1] = pre_data + tempVal
        if contents[i][j] == 'end' and contents[i][j+1] == 'remote':
          index2 = i
          allDevices[name] = contents[index1:index2+1]
          break
  return allDevices


#READ ALL .conf FILES IN /etc/lirc dir
def readConf():
  allDevices = {}
  allConfFiles = []
  contents = []
  allConfFiles = getConfFiles()
  for filename in allConfFiles:
    with open("/etc/lirc/"+filename, "r") as file:
      contents = formatConfFiles(file)
    allDevices = parseConfFile(allDevices, contents)
    del contents[:]
    
  return allDevices

#gather all header information
def getHeaderInfo(file, allDevices):
  headerInfo = {
    "bits":"",
    "zero_pulse":"",
    "zero_space":"",
    "one_pulse":"",
    "one_space":"",
    "pre_data":"",
    "pre_data_bits":"",
    "header_pulse":"",
    "header_space":""
  }

  if file in allDevices:
    for key,value in enumerate(allDevices[file]):
      for x in value:
        if x == 'bits':
          headerInfo["bits"] = allDevices[file][key][1]
        
        elif x == 'zero':
          headerInfo["zero_pulse"] = allDevices[file][key][1]
          headerInfo["zero_space"] = allDevices[file][key][2]
        
        elif x == 'one':
          headerInfo["one_pulse"] = allDevices[file][key][1]
          headerInfo["one_space"] = allDevices[file][key][2]
        
        elif x == 'pre_data':
          headerInfo["pre_data"] = allDevices[file][key][1][2:].upper()
        
        elif x == 'pre_data_bits':
          headerInfo["pre_data_bits"] = allDevices[file][key][1]
        
        elif x == 'header':
          headerInfo["header_pulse"] = allDevices[file][key][1]
          headerInfo["header_space"] = allDevices[file][key][2]

  return headerInfo

#set all global variables from header information
def setHeaderInfo(headerInfo):
  global header_pulse_upper,header_pulse_lower,header_space_upper,header_space_lower,zero_pulse_upper,zero_pulse_lower,zero_space_upper,zero_space_lower,one_pulse_upper,one_pulse_lower,one_space_upper, one_space_lower, bitTotal
  global ZERO_PULSE, ZERO_SPACE, ONE_PULSE, ONE_SPACE, PRE_DATA, PRE_DATA_BITS, BITS
  #setting variables from header info
  if len(headerInfo) > 0:
    ZERO_PULSE = headerInfo["zero_pulse"]
    ZERO_SPACE = headerInfo["zero_space"]
    ONE_PULSE = headerInfo["one_pulse"]
    ONE_SPACE = headerInfo["one_space"]
    PRE_DATA = headerInfo["pre_data"]
    if(headerInfo["bits"] != ""):
      BITS = headerInfo["bits"]
    else:
      BITS = 0
    if(headerInfo["pre_data_bits"] != ""):
      PRE_DATA_BITS = headerInfo["pre_data_bits"]
    else:
      PRE_DATA_BITS = 0
    HEADER_PULSE = headerInfo["header_pulse"]
    HEADER_SPACE = headerInfo["header_space"]
  else:
    return -1
  bitTotal = int(PRE_DATA_BITS) + int(BITS)
  header_pulse_upper = float(HEADER_PULSE) + (float(HEADER_PULSE)*float(PERCENT))
  header_pulse_lower = float(HEADER_PULSE) - (float(HEADER_PULSE)*float(PERCENT))
  header_space_upper = float(HEADER_SPACE) + (float(HEADER_SPACE)*float(PERCENT))
  header_space_lower = float(HEADER_SPACE) - (float(HEADER_SPACE)*float(PERCENT))

  zero_pulse_upper = float(ZERO_PULSE) + (float(ZERO_PULSE)*float(PERCENT))
  zero_pulse_lower = float(ZERO_PULSE) - (float(ZERO_PULSE)*float(PERCENT))
  zero_space_upper = float(ZERO_SPACE) + (float(ZERO_SPACE)*float(PERCENT))
  zero_space_lower = float(ZERO_SPACE) - (float(ZERO_SPACE)*float(PERCENT))

  one_pulse_upper = float(ONE_PULSE) + (float(ONE_PULSE)*float(PERCENT))
  one_pulse_lower = float(ONE_PULSE) - (float(ONE_PULSE)*float(PERCENT))
  one_space_upper = float(ONE_SPACE) + (float(ONE_SPACE)*float(PERCENT))
  one_space_lower = float(ONE_SPACE) - (float(ONE_SPACE)*float(PERCENT))
  return 1


#functions to determine whether value lies between our threshold
def isWithinHeaderPulseRange(value):
  return (float(value) >= header_pulse_lower and float(value) <= header_pulse_upper)
def isWithinHeaderSpaceRange(value):
  return (float(value) >= header_space_lower and float(value) <= header_space_upper)
def isWithinOnePulseRange(value):
  return (float(value) >= one_pulse_lower and float(value) <= one_pulse_upper)
def isWithinOneSpaceRange(value):
  return (float(value) >= one_space_lower and float(value) <= one_space_upper)
def isWithinZeroPulseRange(value):
  return (float(value) >= zero_pulse_lower and float(value) <= zero_pulse_upper)
def isWithinZeroSpaceRange(value):
  return (float(value) >= zero_space_lower and float(value) <= zero_space_upper)

def decode(val, file, allDevices):
  decoded_val = ""
  headerInfo = {}
  final = ""
  count = 0

  headerInfo = getHeaderInfo(file, allDevices)
  if setHeaderInfo(headerInfo) != -1:
    for i in range(len(val)):
      
      #find header information from val data
      if  (i+1 < len(val)) and (isWithinHeaderPulseRange(float(val[i][1])) or isWithinHeaderSpaceRange(float(val[i+1][1]))):
        logger.debug( "HEADER found at i = " + str(i) + " with value = " + str(val[i][1]) ) 
        decoded_val = ""
        #start reading after header is found, increment +2 due to space and pulse pair
        for k in range(i+2,len(val),2):
          logger.debug( "i=" + str(i) + " k=" + str(k) + " len=" + str(len(val)))
          logger.debug("val[k][1] (PULSE-ZERO) = " + str(val[k][1]) + " " + str( zero_pulse_lower ) + " " + str( zero_pulse_upper ))
          logger.debug("val[k+1][1] (SPACE-ZERO) = " + str(val[k+1][1]) + " " + str( zero_space_lower ) + " " + str( zero_space_upper ))
          logger.debug("val[k][1] (PULSE-ONE) = " + str(val[k][1]) + " " + str( one_pulse_lower ) + " " + str( one_pulse_upper ))
          logger.debug("val[k+1][1] (SPACE-ONE) = " + str(val[k+1][1]) + " " + str( one_space_lower ) + " " + str( one_space_upper ))

          if isWithinZeroPulseRange(float(val[k][1])):
            if isWithinZeroSpaceRange(float(val[k+1][1])):
              decoded_val += "0"
              count +=1

          # assume that if the PULSE and SPACE equate to a "0" that they will NOT also equate to a "1"
          if isWithinOnePulseRange(float(val[k][1])):
            if isWithinOneSpaceRange(float(val[k+1][1])):
              decoded_val += "1"
              count +=1
        
          logger.debug("decode_val = " + decoded_val)
          
         # every 4 binary bits we get the hex value
          if count % 4 == 0 and count != 0 :
            try:
              decimal = int(decoded_val,2)
            except:
              return "decoded_val contains an empty char \"\""
            final += str(hex(decimal)[2:])
            decoded_val = ""
          
          logger.debug("count= " + str(count) + " bitTotal=" + str(bitTotal))
          logger.debug("final= " + final.upper())
          if count == bitTotal:
            for key, value in enumerate(allDevices[file]):
              for x in value:
                if x.endswith(final.upper()):
                  return allDevices[file][key][0]
            return "error"
          
  logger.debug("Error: bit count does not equal total bits or config file error")
  return
