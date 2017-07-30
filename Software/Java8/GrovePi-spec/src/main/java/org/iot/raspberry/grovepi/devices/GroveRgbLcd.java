package org.iot.raspberry.grovepi.devices;

import java.io.IOException;
import org.iot.raspberry.grovepi.GroveI2CPin;
import org.iot.raspberry.grovepi.GrovePiSequenceVoid;

@GroveI2CPin
public abstract class GroveRgbLcd implements AutoCloseable {

  public static final int DISPLAY_RGB_ADDR = 0x62;
  public static final int DISPLAY_TEXT_ADDR = 0x3e;

  private static final int LCD_COMMAND = 0x80;
  private static final int LCD_WRITECHAR = 0x40;

  private static final int LCD_CMD_CLEARDISPLAY = 0x01;
  private static final int LCD_CMD_NEWLINE = 0xc0;

  private static final int REG_RED = 0x04;
  private static final int REG_GREEN = 0x03;
  private static final int REG_BLUE = 0x02;

  protected void init() throws IOException {
    execRGB((io) -> {
      io.write(0, 0);
      io.write(1, 0);
      io.write(0x08, 0xaa);
    });
    execTEXT((io) -> {
      io.write(LCD_COMMAND, 0x08 | 0x04); // display on, no cursor
      io.write(LCD_COMMAND, 0x28); // 2 Lines
      io.write(LCD_COMMAND, LCD_CMD_CLEARDISPLAY); // clear Display
      io.sleep(50);
    });
  }

  public void setRGB(int r, int g, int b) throws IOException {
    execRGB((io) -> {
      io.write(REG_RED, r);
      io.write(REG_GREEN, g);
      io.write(REG_BLUE, b);
      io.sleep(50);
    });
  }

  public void setText(String text) throws IOException {
    execTEXT((io) -> {
      io.write(LCD_COMMAND, LCD_CMD_CLEARDISPLAY); // clear Display
      io.sleep(50);
      int count = 0;
      int row = 0;
      for (char c : text.toCharArray()) {
        if (c == '\n' || count == 16) {
          count = 0;
          row += 1;
          if (row == 2) {
            break;
          }
          io.write(LCD_COMMAND, LCD_CMD_NEWLINE); // new line
          if (c == '\n') {
            continue;
          }
        }
        count++;
        io.write(LCD_WRITECHAR, c); // Write character
      }
      io.sleep(100);
    });
  }

  public abstract void execRGB(GrovePiSequenceVoid sequence) throws IOException;

  public abstract void execTEXT(GrovePiSequenceVoid sequence) throws IOException;

  @Override
  public abstract void close();

}
