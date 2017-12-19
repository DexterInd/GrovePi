package grovepi.observer;

/*
 * **********************************************************************
 * PROJECT       :  GrovePi Java Library
 *
 * This file is part of the GrovePi Java Library project. More information about
 * this project can be found here:  https://github.com/DexterInd/GrovePi
 * **********************************************************************
 * 
 * ## License
 * 
 * The MIT License (MIT)
 * GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

import com.dexterind.grovepi.sensors.base.AnalogSensor;
import java.io.IOException;


/**
 * An instance of this class reads sensor data from a GrovePi analog sensor and
 * updates an observer with this data.
 * 
 * @author James Luczynski
 * @author Jeff Blankenship
 */
public class AnalogInputReader extends InputSensorReader implements Runnable{
    private AnalogSensor sensor;
    /**
    * Constructor
    * @param pin the GrovePi port number the sensor is plugged into
    * @throws IOException
    * @throws InterruptedException
    * @throws Exception 
    */   
    public AnalogInputReader(int pin) throws InterruptedException, Exception{
        sensor = new AnalogSensor(pin, 4);
        readDelay = 250;
    }
    /**
     * Constructor
     * @param pin the GrovePi port number the sensor is plugged into
     * @param bufferLength length of byte[] to be read from the sensor
     * @throws InterruptedException
     * @throws Exception 
     */
    public AnalogInputReader(int pin, int bufferLength) throws InterruptedException, Exception{
        sensor = new AnalogSensor(pin, bufferLength);
        readDelay = 250;
    }
    /**
     * Reads the values of the sensor, and notifies this instance's observers
     * of these new values
     */
    public void run() {
        try {
            byte[] newState = sensor.readBytes();
            state = newState;
            notifyObservers(state);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
    /**
     * Begins reading sensor values
     */
    public void startReading(){
        super.startReading(this);
    }
}
