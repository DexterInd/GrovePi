package org.iot.raspberry.examples;

import java.io.File;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.pi4j.GrovePi4J;

public class Runner {

  public static void main(String[] args) throws Exception {
    Logger.getLogger("GrovePi").setLevel(Level.WARNING);
    Logger.getLogger("RaspberryPi").setLevel(Level.WARNING);

    File control = new File("RUNNINGSAMPLES");
    control.deleteOnExit();
    if (control.exists()) {
      control.delete();
      System.out.println("STOPING CURRENT SAMPLE");
      System.exit(0);
    }
    /*
    if (args.length != 2) {
      System.err.println("You need to provide 2 arguments DIO|PI4J EXAMPLECLASS");
      System.exit(-1);
    }
    */
    if (args.length != 1) {
        System.err.println("You need to provide 1 argument - name of the class");
        System.exit(-1);
    }

    control.createNewFile();
    
    /*
    String mode = args[0];
    GrovePi grovePi;
    switch (mode.toLowerCase()) {
      case "pi4j":
        grovePi = new GrovePi4J();
        break;
      case "test":
        grovePi = createProxy(GrovePi.class);
        break;
      default:
        throw new IllegalArgumentException("You must provide either DIO or PI4J implementation");
    }
    */
    
    GrovePi grovePi = new GrovePi4J();
    Example example = (Example) Class.forName("org.iot.raspberry.examples." + args[0]).newInstance();
    System.out.println("RUNNING EXAMPLE: " + args[0] + " USING: PI4J");
    final ExecutorService runner = Executors.newSingleThreadExecutor();
    final ExecutorService consoleMonitor = Executors.newSingleThreadExecutor();
    final ExecutorService fileMonitor = Executors.newSingleThreadExecutor();
    final Semaphore lock = new Semaphore(0);
    final Monitor monitor = new Monitor();

    runner.execute(() -> {
      try {
        example.run(grovePi, monitor);
      } catch (Exception ex) {
        Logger.getLogger(Runner.class.getName()).log(Level.SEVERE, null, ex);
      }
      lock.release();
    });

    consoleMonitor.execute(() -> {
      try (Scanner scanner = new Scanner(System.in)) {
        String command;
        while (!(command = scanner.next()).equalsIgnoreCase("quit")) {
          System.out.println("Command " + command + " not recognized, try quit");
        }
      }
      monitor.stop();
      lock.release();
    });

    fileMonitor.execute(() -> {
      while (control.exists()) {
        try {
          Thread.sleep(100);
        } catch (InterruptedException ex) {
        }
      }
      monitor.stop();
      lock.release();
    });

    lock.acquire();
    runner.shutdown();
    consoleMonitor.shutdownNow();
    fileMonitor.shutdownNow();
    runner.awaitTermination(10, TimeUnit.SECONDS);
    control.delete();
    System.exit(0);
  }

  private static <T> T createProxy(Class<T> aClass) {
    return (T) Proxy.newProxyInstance(aClass.getClassLoader(), new Class<?>[]{aClass}, (Object proxy, Method method, Object[] args1) -> {
      throw new RuntimeException("Test class methods not allowed");
    });
  }
}
