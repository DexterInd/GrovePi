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

import java.util.ArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/**
 * 
 * 
 * @author James Luczynski
 * @author Jeff Blankenship
 * @author Chad Williams
 */
public abstract class InputSensorReader {
    /**
     * Time in milliseconds between consecutive readings of sensor values
     * Each subclass reinitialize this differently in their constructors
     */    
    protected int readDelay = 100; 
    /**
     * The pin number on the GrovePi that this object reads from
     */
    protected int pin;
    /**
     * The list of observers that will be updated with the read values
     */
    protected ArrayList<InputSensorObserver> observers = new ArrayList();
    /**
     * Responsible for making intermittent readings of sensor values
     */
    private ScheduledExecutorService exec;
    /**
     * contains the most recent values read from the sensor
     */
    protected byte[] state = {0};
    
    /**
     * Adds an InputSensorObserver object to the list of observers
     * @param observer the InputSensorObserver object to be added
     */
    public void addObserver(InputSensorObserver observer){
        observers.add(observer);
    }
    /**
     * Removes an InputSensorObserver object to the list of observers
     * @param observer the InputSensorObserver object to be removed
     */        
    public void removeObserver(InputSensorObserver observer){
        observers.remove(observer);
    }
    
    public ArrayList getObservers(){
        return observers;
    }
    /**
     * Begins reading the values of the sensor.
     * @param r 
     */
    protected void startReading(Runnable r){
        exec = Executors.newSingleThreadScheduledExecutor();
        exec.scheduleAtFixedRate(r, 0, readDelay, TimeUnit.MILLISECONDS);
    }    
    /**
     * Stops the intermittent readings of the sensor.
     */
    public void stopReading(){
        if (exec != null)
            exec.shutdown();
    }
    /**
     * Changes the time interval between consecutive reads to the sensor
     * @param delay the new time interval in milliseconds
     */
    public void setDelay(int delay){
        readDelay = delay;
    }
    /**
     * Notifies all observers of this object of the newly read values from the sensor
     * @param b 
     */
    public void notifyObservers(byte[] b){
        for (InputSensorObserver obs : observers)
            obs.update(b);
    }
    /**
     * @param b1 
     * @param b2
     * @return true if both byte[] are equal, false otherwise
     */
    protected static boolean equals(byte[] b1, byte[] b2){
        if (b1.length != b2.length)
            return false;
        else{
            for (int i = 0; i < b1.length; i++)
                if (b1[i] != b2[i])
                    return false;
        }
        return true;
    }
}
