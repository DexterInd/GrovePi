package org.iot.raspberry.examples;

import java.util.concurrent.Semaphore;

public class Monitor {
  
  private Semaphore semaphore = new Semaphore(0);
  private boolean running = true;
  
  public void waitForStop() throws InterruptedException {
    semaphore.acquire();
    semaphore.release();
  }
  
  public void stop() {
    running = false;
    semaphore.release();
  }
  
  public boolean isRunning() {
    return running;
  }
}
