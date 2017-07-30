package com.dexterind.grovepi.utils;

import java.io.IOException;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class Debug {
  private Logger logger;
  private FileHandler fh;

  public static final int FINEST = 1;
  public static final int FINER = 2;
  public static final int FINE = 3;
  public static final int CONFIG = 4;
  public static final int INFO = 5;
  public static final int WARNING = 6;
  public static final int SEVERE = 7;

  private Boolean debug = false;
  private String logDir = "/var/log/grovepi";
  private String logFile = "all.log";

  public Debug(String target) {
    Properties prop = new Properties();
    InputStream input = null;

    try {
      String configProp = System.getProperty("config") == null ? "default" : System.getProperty("config");
      input = new FileInputStream(System.getProperty("user.dir") + "/../config/" + configProp + ".properties");
      prop.load(input);

      debug = Boolean.valueOf(prop.getProperty("debug"));
      logDir = prop.getProperty("logDir");
      logFile = prop.getProperty("logFile");
    } catch (IOException e) {
      e.printStackTrace();
    } finally {
      if (input != null) {
        try {
          input.close();
        } catch (IOException e) {
          e.printStackTrace();
        }
      }
    }

    logger = Logger.getLogger(target);
    try {
      File file = new File(logDir);
      if (!file.exists()) {
        if (file.mkdir()) {
          System.out.println("Log Directory is created!");
        } else {
          System.out.println("Failed to create log directory!");
        }
      }
      fh = new FileHandler(logDir + "/" + logFile, true);
      logger.addHandler(fh);
      logger.setUseParentHandlers(false);
      // this one disables the console log
      SimpleFormatter formatter = new SimpleFormatter();
      fh.setFormatter(formatter);
    } catch (SecurityException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public void log(int level, String message) {
    if (!debug) {
      return;
    }

    switch (level) {
      default:
      case Debug.FINEST:
        logger.finest(message);
        break;
      case Debug.FINER:
        logger.finer(message);
        break;
      case Debug.FINE:
        logger.fine(message);
        break;
      case Debug.CONFIG:
        logger.config(message);
        break;
      case Debug.INFO:
        logger.info(message);
        break;
      case Debug.WARNING:
        logger.warning(message);
        break;
      case Debug.SEVERE:
        logger.severe(message);
        break;
    }
  }
}