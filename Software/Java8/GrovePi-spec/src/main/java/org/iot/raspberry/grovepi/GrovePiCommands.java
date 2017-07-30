package org.iot.raspberry.grovepi;

public class GrovePiCommands {

  public static final int unused = 0;
// Command Format
// digitalRead()command format header 
  public static final int dRead_cmd = 1;
// digitalWrite() command format header
  public static final int dWrite_cmd = 2;
// analogRead() command format header
  public static final int aRead_cmd = 3;
// analogWrite() command format header
  public static final int aWrite_cmd = 4;
// pinMode() command format header
  public static final int pMode_cmd = 5;
// Ultrasonic read
  public static final int uRead_cmd = 7;
// Get firmware version
  public static final int version_cmd = 8;
// Accelerometer (+/- 1.5g) read
  public static final int acc_xyz_cmd = 20;
// RTC get time
  public static final int rtc_getTime_cmd = 30;
// DHT Pro sensor temperature
  public static final int dht_temp_cmd = 40;

// Grove LED Bar commands
// Initialise
  public static final int ledBarInit_cmd = 50;
// Set orientation
  public static final int ledBarOrient_cmd = 51;
// Set level
  public static final int ledBarLevel_cmd = 52;
// Set single LED
  public static final int ledBarSetOne_cmd = 53;
// Toggle single LED
  public static final int ledBarToggleOne_cmd = 54;
// Set all LEDs
  public static final int ledBarSet_cmd = 55;
// Get current state
  public static final int ledBarGet_cmd = 56;

// Grove 4 Digit Display commands
// Initialise
  public static final int fourDigitInit_cmd = 70;
// Set brightness, not visible until next cmd
  public static final int fourDigitBrightness_cmd = 71;
// Set numeric value without leading zeros
  public static final int fourDigitValue_cmd = 72;
// Set numeric value with leading zeros
  public static final int fourDigitValueZeros_cmd = 73;
// Set individual digit
  public static final int fourDigitIndividualDigit_cmd = 74;
// Set individual leds of a segment
  public static final int fourDigitIndividualLeds_cmd = 75;
// Set left and right values with colon
  public static final int fourDigitScore_cmd = 76;
// Analog read for n seconds
  public static final int fourDigitAnalogRead_cmd = 77;
// Entire display on
  public static final int fourDigitAllOn_cmd = 78;
// Entire display off
  public static final int fourDigitAllOff_cmd = 79;

// Grove Chainable RGB LED commands
// Store color for later use
  public static final int storeColor_cmd = 90;
// Initialise
  public static final int chainableRgbLedInit_cmd = 91;
// Initialise and test with a simple color
  public static final int chainableRgbLedTest_cmd = 92;
// Set one or more leds to the stored color by pattern
  public static final int chainableRgbLedSetPattern_cmd = 93;
// set one or more leds to the stored color by modulo
  public static final int chainableRgbLedSetModulo_cmd = 94;
// sets leds similar to a bar graph, reversible
  public static final int chainableRgbLedSetLevel_cmd = 95;

  public static final int pMode_out_arg = 1;
  public static final int pMode_in_arg = 0;
}
