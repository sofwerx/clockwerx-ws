from flask import Flask
from flask import request 
from flask import jsonify
import json
import clockManager
import clockInterface
import logging 

app = Flask( __name__ )

logging.basicConfig(filename='/var/www/clockwerxWS/logs/clockwerx.log', filemode= 'a', level=logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s')

@app.route( '/' )
def welcome():
	logging.debug("Entering welcome")
	try:
		message = 'Welcome to Clockwerx Webservice'
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("Exiting welcome")
	return message

@app.route( '/configurations/', methods=['GET'] )
def configurations():
	logging.debug("Entering configurations")
	try:
		configs = clockManager.getConfigurations()
		return configs
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("Exiting configurations")
	
@app.route( '/power/', methods=['POST'] )
def power():
	logging.debug("Entering power")
	try:
		clockInterface.power()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("Exiting power")
	return 'OK'

@app.route('/powerCycle/', methods=['POST'])
def powerCycle():
    logging.debug("Entering powerCycle") 
    try:
        clockInterface.powerCycle()
    except Exception as e:
        logging.exception("exception occured")
    #If the clockInterface.powerCycle is successful this code should never actually be reached
    logging.debug("Exiting powerCycle")
    return 'OK'

@app.route( '/militaryTime/', methods=['POST'] )
def militaryTime():
	logging.debug("Entering milTime")
	try:
		clockInterface.miltime()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("Exiting milTime")
	return 'OK'

@app.route( '/pause/', methods=['POST'] )
def pause():
	logging.debug("Entering pause")
	try:
		clockInterface.pause()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("exiting pause")
	return 'OK'

@app.route( '/resume/', methods=['POST'] )
def resume():
	logging.debug("Entering resume")
	try:
		clockInterface.pause()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("exiting resume")
	return 'OK'

@app.route( '/stop/', methods=['POST'] )
def stop():
	logging.debug("Entering stop")
	try:
		clockInterface.stop()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("exiting stop")
	return 'OK'

@app.route( '/setTime/', methods=['POST'] )
def setTime():
	logging.debug("entering setTime")
	try:
		clockInterface.setTime()
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("exiting setTime")
	return 'OK'

@app.route( '/dim/', methods=['POST'] )
def dim():
	logging.debug("Entering dim")
	try:
		req_data = request.get_json()
		level = req_data['level']
		logging.debug(level)
		clockInterface.dim(level)
	except Exception as e:
		logging.exception("exception occured")
	logging.debug("exiting dim") 
	return 'OK'

@app.route( '/timer/', methods=['POST'] )
def timer():
	logging.debug("entering timer")  
	try: 
            req_data = request.get_json() 
            req_data = req_data['params']
            hours = int(req_data['hours'])
            minutes = int(req_data['minutes'])
            seconds = int(req_data['seconds'])
            clockInterface.timer(hours,minutes,seconds)
	except Exception as e:
		logging.exception("exception occured") 
	logging.debug("exiting timer")
	return 'OK'

