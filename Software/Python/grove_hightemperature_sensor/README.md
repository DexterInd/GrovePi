## Calibrating the Grove High Temperature sensor

##### Attention: 
This `README.md` is only for calibrating the probe and not the onboard  sensor. So, this sensor comes with 2 thermometers:
1. One which is for measuring room temperatures - that's found on the onboard.
2. Another one which is for measuring temperatures between `-50 °C` and `+650 °C` - it's the long metal wire. **This is the one we're calibrating.**

## Step 1
Make the `GrovePi` continously read an analog port and print it in the console. The analog port should be that of the `Grove High Temperature Sensor's`. 

## Step 2
Put the sensor's long wire into a cup of boiling/hot water and take note of the value that's printed in the `Raspberry Pi`'s console. At the same time, use a professional thermometer and measure the temperature and write it down.

Do the same thing with cold water.

## Step 3
We will now have 4 values written down in a note: 
* 2 values that were printed in the `Raspberry Pi`'s console - these values correspond with the following 2 values. 
* 2 values where the measurement unit is in `Celsius Degrees`.

Now, take the values that were measured with the professional thermometer and get them translated with the table provided in `thermocouple_table.json` file.
I.e: In `thermocouple_table.json` file, `90 °C` corresponds to `3.682`.

Now, lets assign the following variables to each of these values:
* `i1` = the translated value (from the table) we got when we measured the hot water w/ the **professional thermometer**.
* `i2` = the translated value (from the table) we got when we measured the cold water w/ the **professional thermometer**.
* `o1` = the translated value (from the table) we got when we measured the hot water w/ **our sensor**.
* `o2` = the translated value (from the table) we got when we measured the cold water w/ **our sensor**.

## Step 4

Let's calculate an `offset` and a `factor`. We will insert the calculated values in our table.

First, lets calculated the `offset`.
* `offset` = `(i1 * o2 - i2 * o1) / (o2 - o1)`

And then, we get to calculate the `factor`. Use the `offset` value for calculating the `factor`.
* `factor` = `(i1 - offset) / o1`

## Step 5

Open up `thermocouple_table.json` file and update the following values:
* For `amp_offset` set the value we got for `offset` - it's preferable to have up to 6-7 digits in precision.
* For `amp_factor` set the value we got for `factor` - it's preferable to have up to 6-7 digits in precision.

Save the modifications.

## Step 6

Run the `high_temperature_example.py` program. 
It's going to use the newly updated values.

------
###### `Note 1`: Calibrate the sensor when the values don't match with a professional thermometer by a long shot (i.e. 10 degrees). The sensor has already been calibrated, but who knows.
###### `Note 2`: The sensor's precision is around `+-3 Celsius Degrees`.
