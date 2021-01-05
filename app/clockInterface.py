import os
import sys
import time
from datetime import datetime
import logging
import subprocess
import irsend
logger = logging.getLogger()

send = "irsend SEND_ONCE lircd.conf KEY_"
 
def dim(dimlevel):
        #os.system(send+str(dimlevel))
        send("KEY_" + str(dimlevel))
        """
        i = 1
	plus = send + "+"
	minus = send + "-"
	
	if dimlevel > 0 and dimlevel < 8:
    		os.system(minus)
    		os.system(minus)
    		os.system(minus)
    		os.system(minus)
    		os.system(minus)
    		os.system(minus)
    		os.system(minus)
	while i < dimlevel:
        	os.system(plus)
        	i += 1
        """
def clockPower():
        #os.system('irsend SEND_ONCE lircd.conf KEY_POWER')
        power = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_POWER"]

        logger.debug( power )
        subprocess.call( power )

        #time.sleep(1)

        logger.debug( power )
        subprocess.call( power )

def power():
        clockPower()
        # os.system('sudo kill $(pidof lircd)')
	    # #time.sleep(1)
        # os.system('sudo lircd --device /dev/lirc0')
	    # #time.sleep(1)
	    # os.system('irsend SEND_ONCE lircd.conf KEY_POWER')
        os.system("sshpass -p'2wsxcde3@WSXCDE#' ssh -tt -o stricthostkeychecking=no swx_pi@192.168.12.135 sudo reboot ")

def powerCycle():
        clockPower()
        os.system("sshpass -p'2wsxcde3@WSXCDE#' ssh -tt -o stricthostkeychecking=no swx_pi@192.168.12.135 sudo reboot ")

def miltime():
        mil = send + '0'
        logger.debug(mil)
        os.system(mil)

def pause():	
        play = send + "PLAY"
        logger.debug(play)
        os.system(play)

def resume():
        play = send + "PlAY"
        logger.debug(play)
        os.system(play)

def stop():
        #cd_set = send + "CD-SET"
        cd_set = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_CD-SET"]

        #ret = send + "RETURN"
        ret = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_RETURN"]

        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)
	
        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)
	
        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)
	
        logger.debug(ret)
        #os.system(ret)
        subprocess.call( ret )
        #time.sleep(1)

def setTime():
        #cd_set = send + "CD-SET"
        cd_set = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_CD-SET"]

        #mode = send + "MODE"
        mode = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_MODE"]

        #t_set = send + "T-SET"
        t_set = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_T-SET"]

        #mode = send + "MODE"
        mode = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_MODE"]

        currentTime = str(datetime.now())
	
        #digit1 = send + currentTime[11]
        digit1 = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_" + currentTime[11]]
        #digit2 = send + currentTime[12]
        digit2 = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_" + currentTime[12]]
        #digit3 = send + currentTime[14]
        digit3 = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_" + currentTime[14]]
        #digit4 = send + currentTime[15]
        digit4 = ["irsend", "SEND_ONCE", "lircd.conf", "KEY_" + currentTime[15]]
        
        logger.debug(t_set)
        #os.system(t_set)
        subprocess.call( t_set )
        #time.sleep(1)
        
        logger.debug(digit1)
        #os.system(digit1)
        subprocess.call( digit1 )
        #time.sleep(1)
        
        logger.debug(digit2)
        #os.system(digit2)
        subprocess.call( digit2 )
        #time.sleep(1)
        
        logger.debug(mode)
        #os.system(mode)
        subprocess.call( mode )
        #time.sleep(1)
        
        logger.debug(digit3)
        #os.system(digit3)
        subprocess.call( digit3 )
        #time.sleep(1)
        
        logger.debug(digit4)
        #os.system(digit4)
        subprocess.call( digit4 )
        #time.sleep(1)
        
        logger.debug(mode)
        #os.system(mode)
        subprocess.call( mode )
        #time.sleep(1)

        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)

        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)
        
        logger.debug(cd_set)
        #os.system(cd_set)
        subprocess.call( cd_set )
        #time.sleep(1)
        
def timer (hours=0,minutes=0,seconds=0):
        #cd_set = send + "CD-SET"
        cd_set = "KEY_CD-SET"

        #mode = send + "MODE"
        mode = "KEY_MODE"

        #play = send + "PLAY"
        play = "KEY_PLAY"

        if (hours > 24 or hours < 0):
                hours=23
                minutes=59
                seconds=0
        if (minutes > 60 or minutes < 0):
                minutes = 59
        if (seconds > 60 or seconds < 0):
                seconds = 59
        if (hours < 10):
                d1 = 0
                d2 = hours
        else:
                d2=hours%10
                d1=int(hours/10)
        if (minutes<10):
                d3 = 0
                d4 = minutes
        else:
                d4=minutes%10
                d3=int(minutes/10)
        if(seconds<10):
                d5=0
                d6=seconds
        else:
                d6=seconds%10
                d5=int(seconds/10)

        #Set timer with provided perame$
        logger.debug(cd_set)
        #os.system(cd_set)
        if not send( cd_set ):
            return timer(hours,minutes,seconds)
        #time.sleep(1)
        
        logger.debug(cd_set)
        #os.system(cd_set)
        if not send( cd_set ):
            return timer(hours,minutes,seconds)
        #time.sleep(1)
        
        logger.debug(mode)
        #os.system(mode)
        if not send( mode ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        logger.debug(mode)
        #os.system(mode)
        if not send( mode ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        #digit1 = send +str(d1)
        digit1 = "KEY_" + str(d1)
        logger.debug(digit1)
        #os.system(digit1)
        if not send( digit1 ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)

        #digit2 = send +str(d2)
        digit2 = "KEY_" + str(d2)
        logger.debug(digit2)
        #os.system(digit2)
        if not send( digit2 ):
             return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        logger.debug(mode)
        #os.system(mode)
        if not send( mode ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        #digit3 = send+str(d3)
        digit3 = "KEY_" + str(d3)
        logger.debug(digit3)
        #os.system(digit3)
        if not send( digit3 ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        #digit4 = send+str(d4)
        digit4 = "KEY_" + str(d4)
        logger.debug(digit4)
        #os.system(digit4)
        if not send( digit4 ):
            return timer(hours,minutes,seconds)

        ##time.sleep(1)

        logger.debug(mode)        
        #os.system(mode)
        if not send( mode ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        #digit5 = send +str(d5)
        digit5 = "KEY_" + str(d5)
        logger.debug(digit5)   
        #os.system(digit5)
        if not send( digit5 ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)
        
        #digit6 = send +str(d6)
        digit6 = "KEY_" + str(d6)
        logger.debug(digit6)  
        #os.system(digit6)
        if not send( digit6 ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)

        logger.debug(play) 
        #os.system(play)
        if not send( play ):
            return timer(hours,minutes,seconds)

        #time.sleep(1)


def send(keyName):
        deviceName = "lircd.conf"
        count = 0
        isOk = False
        #while count < 5 and not isOk :
        isOk = irsend.irsend(deviceName, keyName)
        logger.debug(isOk)
        #time.sleep(0.5)
                #count += 1
        return isOk
