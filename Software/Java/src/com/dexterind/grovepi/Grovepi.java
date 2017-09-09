package com.dexterind.grovepi;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.sensors.*;
import com.dexterind.grovepi.events.*;
import com.dexterind.grovepi.utils.*;

public final class Grovepi {
  private static Grovepi instance;

  private boolean isInit = false;
  private boolean isHalt = false;

  public Board board;
  private final CopyOnWriteArrayList<GrovepiListener> listeners;

  private Debug debug;

  public Grovepi() throws Exception {
    debug = new Debug("com.dexterind.gopigo.Grovepi");
    debug.log(Debug.FINEST, "Instancing a new GrovePi");

    try {
      board = Board.getInstance();
    } catch (IOException e) {
      e.printStackTrace();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }

    listeners = new CopyOnWriteArrayList<GrovepiListener>();
  }

  public static Grovepi getInstance() {
    if(instance == null) {
      try {
        instance = new Grovepi();
      }
      catch (Exception e) {
        System.out.println("There was an error");
      }
    }
    return instance;
  }

  public void init() {
    debug.log(Debug.FINE, "Init " + isInit);
    board.init();
    isInit = true;
    StatusEvent statusEvent = new StatusEvent(this, Statuses.INIT);
    fireEvent(statusEvent);
  }

  public void addListener(GrovepiListener listener) {
    debug.log(Debug.INFO, "Adding listener");
    listeners.addIfAbsent(listener);
  }

  public void removeListener(GrovepiListener listener) {
    if (listeners != null) {
      debug.log(Debug.INFO, "Removing listener");
      listeners.remove(listener);
    }
  }

  protected void fireEvent(EventObject event) {
    int i = 0;
    debug.log(Debug.INFO, "Firing event [" + listeners.toArray().length + " listeners]");

    for (GrovepiListener listener : listeners) {
      debug.log(Debug.INFO, "listener[" + i + "]");
      debug.log(Debug.INFO, event.getClass().toString());

      if (event instanceof StatusEvent) {
        listener.onStatusEvent((StatusEvent) event);
      } else if (event instanceof SensorEvent) {
        listener.onSensorEvent((SensorEvent) event);
      }
      i++;
    }
  }
}
