#include "grovepi.h"

int main()
{
	int current_retries = 0; // current number of I2C errors encountered
	int max_retries = 5; // maximum number of consecutive I2C errors

	int sound_sensor_pin = 0; // analog port A0 for the Grove Sound Sensor
	int LED_pin = 5; // digital port D5 for the Grove LED
	int threshold_value = 400; // threshold value for the sound levels (values from 0 -> 1023)
	int sensor_value; // variable to hold the Sound Sensor's value

	// set the LED & Sound pins accordingly
	pinMode(sound_sensor_pin, INPUT);
	pinMode(LED_pin, OUTPUT);


	// start reading the value on the Sound sensor
	sensor_value = analogRead(sound_sensor_pin);
	// while I2C error threshold not hit
	while(current_retries < max_retries)
	{
		if(sensor_value == -1)
		{
			current_retries += 1;
		}
		else
		{
			// reset the counter since we care
			// about the consecutives
			current_retries = 0;
			// check whether we turn the LED ON or OFF
			// based on the threshold value
			if(sensor_value > threshold_value)
				digitalWrite(LED_pin, HIGH);
			else
				digitalWrite(LED_pin, LOW);

			// and print the sensor value onto the terminal
			printf("[sensor value = %d]\n", sensor_value);
		}

		// and wait 500 ms for the next reading
		delay(500);
		sensor_value = analogRead(sound_sensor_pin);
	}

	printf("[I2C errors threshold hit]\n");

	return 0;
}
