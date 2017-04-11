#include "grovepi.h"

int main()
{
	int current_retries = 0; // current number of I2C errors encountered
	int max_retries = 5; // maximum number of consecutive I2C errors

	int light_sensor_pin = 0; // analog port A0 for the Grove Light Sensor
	int LED_pin = 4; // digital port D4 for the Grove LED
	int threshold = 10; // threshold value in kOhm for the Grove Light Sensor
	int sensor_value; // variable to hold the Grove Light Sensor value
	float resistance; // variable to hold the Grove Light Sensor's resistance value

	// set the LED & Light pins accordingly
	pinMode(light_sensor_pin, INPUT);
	pinMode(LED_pin, OUTPUT);

	// start reading the value on the Light Sensor
	sensor_value = analogRead(light_sensor_pin);
	// while I2C error stays below the threshold
	while(current_retries < max_retries)
	{
		// if error occured during reading
		if(sensor_value == -1)
		{
			// then increase the retry counter
			current_retries += 1;
		}
		else
		{
			// otherwise reset the counter
			current_retries = 0;
			// calculate the resistance
			resistance = (float)(1023 - sensor_value) * 10 / sensor_value;

			// check if the resistance gets beyond the threshold
			// value in kOhm (check how a light sensor works)
			// and turn ON/OFF the LED on the associated pin accordingly
			if(resistance > threshold)
				digitalWrite(LED_pin, HIGH);
			else
				digitalWrite(LED_pin, LOW);

			// and finally print the
			printf("[sensor value = %d][resistance = %.2f]\n", sensor_value, resistance);
		}

		// wait half a second for the next reading
		delay(500);
		sensor_value = analogRead(light_sensor_pin);
	}

	return 0;
}
