package org.iot.raspberry.grovepi;

public interface GroveDigitalInListener {

  void onChange(boolean oldValue, boolean newValue);
}
