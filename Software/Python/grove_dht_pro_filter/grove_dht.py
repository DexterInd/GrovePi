import threading # we need threads for processing data seperately from the main thread
import numpy # for statistical computations
import datetime
import math # for NaNs
from grovepi import dht # we built on top of the base function found in the grovepi library
from grovepi import statisticalNoiseReduction # importing function which is meant for removing outliers from a given set
import time


'''
# after a list of numerical values is provided
# the function returns a list with the outlier(or extreme) values removed
# make the std_factor_threshold bigger so that filtering becomes less strict
# and make the std_factor_threshold smaller to get the opposite
def statisticalNoiseReduction(values, std_factor_threshold = 2):
	if len(values) == 0:
		return []

	mean = numpy.mean(values)
	standard_deviation = numpy.std(values)

	# just return if we only got constant values
	if standard_deviation == 0:
		return values

	# remove outlier values which are less than the average but bigger than the calculated threshold
	filtered_values = [element for element in values if element > mean - std_factor_threshold * standard_deviation]
	# the same but in the opposite direction
	filtered_values = [element for element in filtered_values if element < mean + std_factor_threshold * standard_deviation]

	return filtered_values
'''

# class for the Grove DHT sensor
# it was designed so that on a separate thread the values from the DHT sensor are read
# on the same separate thread, the filtering process takes place
class Dht(threading.Thread):
	# refresh_period specifies for how long data is captured before it's filtered
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

		self.last_temperature = None
		self.last_humidity = None

	# refresh_period specifies for how long data is captured before it's filtered
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

	# removes the processed data from the buffer
	def clearBuffer(self):
		self.lock.acquire()
		self.filtered_humidity = []
		self.filtered_temperature = []
		self.lock.release()

	# the bigger the parameter, the less strict is the filtering process
	# it's also vice-versa
	def setFilteringAggresiveness(self, filtering_aggresiveness = 2):
		self.filtering_aggresiveness = filtering_aggresiveness

	# whenever there's new data processed
	# a callback takes place
	# arguments can also be sent
	def setCallbackFunction(self, callbackfunc, *args):
		self.callbackfunc = callbackfunc
		self.args = args

	# stops the current thread from running
	def stop(self):
		self.event_stopper.set()
		self.join()

	# replaces the need to custom-create code for outputting logs/data
	# print(dhtObject) can be used instead
	def __str__(self):
		string = ""
		self.lock.acquire()
		# check if we have values in the buffer
		if len(self.filtered_humidity) > 0:
			self.last_temperature = self.filtered_temperature.pop()
			self.last_humidity = self.filtered_humidity.pop()
		self.lock.release()

		# retrieve the last read value
		if not self.last_humidity is None:
			string = '[{}][temperature = {:.01f}][humidity = {:.01f}]'.format(
			datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			self.last_temperature, self.last_humidity)

		# otherwise it means we haven't got values yet
		else:
			string = '[{}][waiting for buffer to fill]'.format(
			datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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

	# you musn't call this function from the user-program
	# this one is called by threading.Thread's start function
	def run(self):
		values = []

		# while we haven't called stop function
		while not self.event_stopper.is_set():
			counter = 0

			# while we haven't done a cycle (period)
			while counter < self.refresh_period and not self.event_stopper.is_set():
				temp = None
				humidity = None

				# read data
				try:
					[temp, humidity] = dht(self.pin, self.sensor_type)

					# check for NaN errors
					if math.isnan(temp) is False and math.isnan(humidity) is False:
						new_entry = {"temp" : temp, "hum" : humidity}
						values.append(new_entry)

					else:
						raise RuntimeWarning("[dht sensor][we've caught a NaN]")

					counter += 1

				# in case we have an I2C error
				except IOError:
					if self.debugging is True:
						print("[dht sensor][we've got an IO error]")

				# intented to catch NaN errors
				except RuntimeWarning as error:
					if self.debugging is True:
						print(str(error))

				finally:
					# the DHT can be read once a second
					time.sleep(1)

			if len(values) > 0:
				# remove outliers
				temp = numpy.mean(statisticalNoiseReduction([x["temp"] for x in values], self.filtering_aggresiveness))
				humidity = numpy.mean(statisticalNoiseReduction([x["hum"] for x in values], self.filtering_aggresiveness))

				# insert into the filtered buffer
				self.lock.acquire()
				self.filtered_temperature.append(temp)
				self.filtered_humidity.append(humidity)
				self.lock.release()

				# if we have set a callback then call that function w/ its parameters
				if not self.callbackfunc is None:
					self.callbackfunc(*self.args)

			# reset the values for the next iteration/period
			values = []

		if self.debugging is True:
			print("[dht sensor][called for joining thread]")
