package org.iot.raspberry.grovepi;

public interface GroveAnalogInListener {

  void onChange(byte[] newValue);
}
