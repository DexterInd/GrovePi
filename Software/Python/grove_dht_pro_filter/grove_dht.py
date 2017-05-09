import threading
import numpy
import datetime
import math
from grovepi import dht
import time


'''
# provide an array of data for filtering through [values]
# [std_factor_threshold] represents the multiplier of the calculated standard_deviation
# through [std_factor_threshold] we set an upper & lower threshold for these data values
# therefore this function removes outlier values which go beyond the calculated threshold
# the default [std_factor_threshold] should be enough for most sensor filterings
# the bigger the [std_factor_threshold] the more strict is the filtering
# the lower the [std_factor_threshold] the lest strict is the filtering
def statisticalNoiseReduction(values, std_factor_threshold = 2):
	mean = numpy.mean(values)
	standard_deviation = numpy.std(values)

	if standard_deviation == 0:
		return values

	filtered_values = [element for element in values if element > mean - std_factor_threshold * standard_deviation]
	filtered_values = [element for element in filtered_values if element < mean + std_factor_threshold * standard_deviation]

	return filtered_values
'''

# class for the Grove DHT Pro sensor
# the class instance runs on a separate thread
# the separate thread reads the data of the sensor
# while in the main thread we can trigger actions based on what we read
class Dht(threading.Thread):
	# [pin] is the digital port to which the DHT sensor is connected and the it defaultly points to digital port 4
	# [refresh_period] is the amount of time it reads data before it filters it
	# [debugging] is True/False depending on whether you want on-screen debugging
	# The default sensor we're using is the Grove Dht Pro Blue module (you can change it to the white one)
	def __init__(self, pin = 4, refresh_period = 10.0, debugging = False):
		super(Dht, self).__init__(name = "DHT filtering")

		self.pin = pin
		self.refresh_period = refresh_period
		self.debugging = debugging
		self.event_stopper = threading.Event()

		self.blue_sensor = 0
		self.white_sensor = 1
		self.filtering_aggresiveness = 2
		self.callbackfunc = None
		self.sensor_type = self.blue_sensor

		self.lock = threading.Lock()

		self.filtered_temperature = []
		self.filtered_humidity = []

	# sets for how much time (in seconds) we read data before we filter it
	# the bigger the period of time, the better is the data filtered
	def setRefreshPeriod(self, time):
		self.refresh_period = time

	# sets the digital port
	def setDhtPin(self, pin):
		self.pin = pin

	# use the white sensor module
	def setAsWhiteSensor(self):
		self.sensor_type = self.white_sensor

	# use the blue sensor module
	def setAsBlueSensor(self):
		self.sensor_type = self.blue_sensor

	# clears the buffer of filtered data
	# useful when you got too much data inside of it
	def clearBuffer(self):
		self.lock.acquire()
		self.filtered_humidity = []
		self.filtered_temperature = []
		self.lock.release()

	# sets how aggresive the filtering has to be
	# read more about [statisticalNoiseReduction] function, because
	# we're basically setting the parameter for it
	def setFilteringAggresiveness(self, filtering_aggresiveness = 2):
		self.filtering_aggresiveness

	# callback function
	# whenever we have newly filtered data
	# it calls the parameter-sent function
	# you can also send variable-length parameters for the
	# callback function through [*args] parameter
	def setCallbackFunction(self, callbackfunc, *args):
		self.callbackfunc = callbackfunc
		self.args = args

	# stops the current thread from running
	def stop(self):
		self.event_stopper.set()
		self.join()

	# is useful when you want to print the data using
	# the built-in [print] function
	# it prints a nicely formatted text with the data
	def __str__(self):
		string = ""
		if len(self.filtered_humidity) > 0:
			string = '[{}][temperature = {:.01f}][humidity = {:.01f}]'.format(
			datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			self.filtered_temperature.pop(),
			self.filtered_humidity.pop())

		return string

	# returns a tuple with the (temperature, humidity) format
	# if there's nothing in the buffer, then it returns (None, None)
	def feedMe(self):

		if self.length() > 0:
			self.lock.acquire()
			temp = self.filtered_temperature.pop()
			hum = self.filtered_humidity.pop()
			self.lock.release()
			return (temp, hum)
		else:
			return (None, None)

	# returns the length of the buffer
	# the buffer is filled with filtered data
	def length(self):
		self.lock.acquire()
		length = len(self.filtered_humidity)
		self.lock.release()
		return length

	# we've overwritten the Thread.run method
	# so we can process / filter data inside of it
	# you don't need to care about it
	def run(self):
		values = []

		while not self.event_stopper.is_set():
			counter = 0
			while counter < self.refresh_period and not self.event_stopper.is_set():
				temp = None
				humidity = None

				try:
					[temp, humidity] = dht(self.pin, self.sensor_type)

					if math.isnan(temp) is False and math.isnan(humidity) is False:
						new_entry = {"temp" : temp, "hum" : humidity}
						values.append(new_entry)

					else:
						raise RuntimeWarning("[dht sensor][we've caught a NaN]")

				except IOError:
					if self.debugging is True:
						print("[dht sensor][we've got an IO error]")

				except RuntimeWarning as error:
					if self.debugging is True:
						print(str(error))

				finally:
					time.sleep(1)
					counter += 1

			# the next following lines insert the filtered data inside 2 lists
			temp = numpy.mean(statisticalNoiseReduction([x["temp"] for x in values], self.filtering_aggresiveness))
			humidity = numpy.mean(statisticalNoiseReduction([x["hum"] for x in values], self.filtering_aggresiveness))

			self.lock.acquire()
			self.filtered_temperature.append(temp)
			self.filtered_humidity.append(humidity)
			self.lock.release()

			# function for callbacking the supplied function
			if not self.callbackfunc is None:
				self.callbackfunc(*self.args)

			values = []

		if self.debugging is True:
			print("[dht sensor][called for joining thread]")
