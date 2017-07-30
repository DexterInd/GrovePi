package tests;

import com.dexterind.grovepi.*;
import com.dexterind.grovepi.sensors.base.*;
import com.dexterind.grovepi.sensors.*;
import com.dexterind.grovepi.events.*;
import com.dexterind.grovepi.utils.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class BaseTest implements GrovepiListener {
  private static Grovepi grovepi = null;

  public BaseTest() throws IOException, InterruptedException, Exception {
    System.out.println("-----------------------------------------------------");
    System.out.println(" GrovePi test application");
    System.out.println("----------------------------------------------------");

    grovepi = Grovepi.getInstance();
    grovepi.addListener(this);
    grovepi.init();
  }
  
  public void onStatusEvent(StatusEvent event) {
	if (event.status == 2) {
		
		try {
			System.out.print( grovepi.board.version() );
		} catch( IOException e) {
			System.out.print( e.getMessage() );
		}
		
		try {
			System.out.print( "\n" );
			this.getDHTValue();
			System.out.print( "\n" );
		} catch ( Exception e) {
			System.out.print( "Err:" + e.getMessage() );
		}
	}
  };
  public void onSensorEvent(SensorEvent event) {
	System.out.print(event.value);
  };
  
  public void getDHTValue() throws IOException, InterruptedException, Exception {
	int pin = 2; // D2
	DHTDigitalSensor sensor = new DHTDigitalSensor(
								pin,
								DHTDigitalSensor.MODULE_DHT22,
								DHTDigitalSensor.SCALE_C
							);
	float[] output = sensor.read();
	System.out.print( Arrays.toString(output) );
  }

}
