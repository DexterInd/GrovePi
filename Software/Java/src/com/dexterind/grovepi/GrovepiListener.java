package com.dexterind.grovepi;

import com.dexterind.grovepi.events.*;
import java.util.EventListener;

public interface GrovepiListener extends EventListener {
  public void onStatusEvent(StatusEvent event);
  public void onSensorEvent(SensorEvent event);
}
