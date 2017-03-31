package org.iot.raspberry.grovepi;

public class GroveUtil {

  public static int[] unsign(byte[] b) {
    int[] v = new int[b.length];
    for (int i = 0; i < b.length; i++) {
      v[i] = unsign(b[i]);
    }
    return v;
  }

  public static int unsign(byte b) {
    return b & 0xFF;
  }
}
