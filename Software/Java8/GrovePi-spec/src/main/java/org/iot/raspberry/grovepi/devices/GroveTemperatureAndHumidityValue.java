package org.iot.raspberry.grovepi.devices;

public class GroveTemperatureAndHumidityValue {

  private final double temperature;
  private final double humidity;

  public GroveTemperatureAndHumidityValue(double temperature, double humidity) {
    this.temperature = temperature;
    this.humidity = humidity;
  }

  public double getTemperature() {
    return temperature;
  }

  public double getHumidity() {
    return humidity;
  }

  @Override
  public String toString() {
    return "temperature=" + temperature + ", humidity=" + humidity;
  }

}
