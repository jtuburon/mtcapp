from openmtc_app import DA
from openmtc_app.flask_runner import FlaskRunner
import time

import sys
import Adafruit_DHT

class MyDA(DA):
	def read_sensor_data(self):
		sensor_args = {'11': Adafruit_DHT.DHT11,
		'22': Adafruit_DHT.DHT22,
		'2302': Adafruit_DHT.AM2302 }
		sensor = sensor_args['11']
		gpio = 4
		humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
		return {
			"humidity": humidity, 
			"temperature":temperature
		}

	def _on_register(self):
		container= self.create_container(None, "myContainer")
		while True:
			sensor_data = self.read_sensor_data()
			data = {
				"data": sensor_data
			}
			print data
			self.push_content(container, data)
			time.sleep(10)

app_instance = MyDA() 
runner = FlaskRunner(app_instance)

GSCL_URL="http://192.168.254.128:4000"
runner.run(GSCL_URL) 