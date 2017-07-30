package org.iot.raspberry.examples;

import java.io.IOException;
import java.util.Random;
import org.iot.raspberry.grovepi.GrovePi;
import org.iot.raspberry.grovepi.devices.GroveRgbLcd;

public class RgbLcd implements Example {

  @Override
  public void run(GrovePi grovePi, Monitor monitor) throws Exception {
    GroveRgbLcd lcd = grovePi.getLCD();

    String[] phrases = new String[]{
      "Hi! ALL!",
      "This should work just fine",
      "A message\nA response",
      "More data that you can handle for sure!",
      "Welcome to the internet of things with java",
      "Short\nMessage"
    };
    int[][] colors = new int[][]{
      {50, 255, 30},
      {15, 88, 245},
      {248, 52, 100},
      {48, 56, 190},
      {178, 25, 180},
      {210, 210, 210}
    };
    while (monitor.isRunning()) {
      try {
        String text = phrases[new Random().nextInt(phrases.length)];
        int[] color = colors[new Random().nextInt(colors.length)];
        lcd.setRGB(color[0], color[1], color[2]);
        Thread.sleep(100);
        lcd.setText(text);
        Thread.sleep(2000);
      } catch (IOException io) {
      }
    }
  }

}
