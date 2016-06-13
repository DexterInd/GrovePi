package com.dexterind.grovepi.events;

import java.util.EventObject;

public class StatusEvent extends EventObject {

  private static final long serialVersionUID = -2236533038040111378L;
  public int status;

  public StatusEvent(Object source) {
	  super(source);
  }

  public StatusEvent(Object source, int status) {
	  this(source);
	  this.status = status;
  }
}