package org.iot.raspberry.grovepi.devices;

public class GroveRotaryValue {

  private final double sensorValue;
  private final double voltage;
  private final double degrees;

  public GroveRotaryValue(double sensorValue, double voltage, double degrees) {
    this.sensorValue = sensorValue;
    this.voltage = voltage;
    this.degrees = degrees;
  }

  public double getSensorValue() {
    return sensorValue;
  }

  public double getVoltage() {
    return voltage;
  }

  public double getDegrees() {
    return degrees;
  }

  @Override
  public String toString() {
    return "S:" + sensorValue + ",V:" + voltage + ",D:" + getDegrees();
  }

  /**
   * 0 to 1 factor
   *
   * @return a number between 0 and 1
   */
  public double getFactor() {
    return (getDegrees() / GroveRotarySensor.FULL_ANGLE);
  }
}
