package org.iot.raspberry.grovepi.devices;

public interface GroveInputDeviceListener<T> {

  void onChange(T t);
}
