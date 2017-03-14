package org.iot.raspberry.grovepi;

import java.io.IOException;
import static org.iot.raspberry.grovepi.GrovePiCommands.*;

public class GroveAnalogOut {

  private final GrovePi grovePi;
  private final int pin;

  public GroveAnalogOut(GrovePi grovePi, int pin) throws IOException {
    this.grovePi = grovePi;
    this.pin = pin;
    grovePi.execVoid((GroveIO io) -> io.write(pMode_cmd, pin, pMode_out_arg, unused));
  }

  public void set(double value) throws IOException {
    int[] command = new int[8];
    command[0] = aWrite_cmd;
    command[1] = pin;
    command[2] = 1;
    command[3] = 3;
    command[4] = unused;
    grovePi.execVoid((GroveIO io) -> io.write(command));
  }

}
