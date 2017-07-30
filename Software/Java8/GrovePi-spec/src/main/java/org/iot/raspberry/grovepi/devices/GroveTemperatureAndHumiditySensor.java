package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import java.nio.ByteBuffer;
import org.iot.raspberry.grovepi.GroveDigitalPin;
import org.iot.raspberry.grovepi.GrovePi;
import static org.iot.raspberry.grovepi.GrovePiCommands.*;

@GroveDigitalPin
public class GroveTemperatureAndHumiditySensor {

  public enum Type {

    DHT11(0), //blue one
    DHT22(1), //White one (PRO) AKA (AM2302)
    DHT21(2), //Black One AKA (AM2301)
    AM2301(3); //White one (PRO)
    private final int moduleType;

    private Type(int moduleType) {
      this.moduleType = moduleType;
    }

    public int getModuleType() {
      return moduleType;
    }

  }
  private final GrovePi grovePi;
  private final int pin;
  private final Type dhtType;

  public GroveTemperatureAndHumiditySensor(GrovePi grovePi, int pin, Type dhtType) {
    this.grovePi = grovePi;
    this.pin = pin;
    this.dhtType = dhtType;
  }

  public GroveTemperatureAndHumidityValue get() throws IOException {
    byte[] data = grovePi.exec((io) -> {
      io.write(dht_temp_cmd, pin, dhtType.moduleType, unused);
      io.sleep(600);
      return io.read(new byte[9]);
    });
    double temp = ByteBuffer.wrap(new byte[]{data[4], data[3], data[2], data[1]}).getFloat();
    double humid = ByteBuffer.wrap(new byte[]{data[8], data[7], data[6], data[5]}).getFloat();
    return new GroveTemperatureAndHumidityValue(temp, humid);
  }

}
