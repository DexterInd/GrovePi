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

/**
 * RotaryAngleDeterminer.
 * This GrovePi sensor demonstration is part of a coursework project
 * for CS505 Design Patterns, at Central Connecticut State University,
 * Fall 2017, with Dr. Chad Williams.
 * 
 * @author James Luczynski
 * @author Jeff Blankenship
 * @author Chad Williams
 */
public class RotaryAngleDeterminer implements InputSensorObserver{
    /**
     * Reference voltage of ADC is 5v
     */
    private static final double ADC_REF = 5;
    /**
     * Vcc of the grove interface is 5 volts
     */
    private static final double GROVE_VCC = 5;
    /**
     * Grove rotary sensor has only 300 degrees of rotation
     */
    private static final double FULL_ANGLE = 300;
    
    private RotaryInvoker invoker;
    
    /**
     * Constructor
     * @see RotaryInvoker
     * @param invoker 
     */
    public RotaryAngleDeterminer(RotaryInvoker invoker){
        this.invoker = invoker;
    }
    /**
     * Changes this instance's rotaryInvoker object to the one in the argument provided.
     * @param invoker 
     */
    public void setInvoker(RotaryInvoker invoker){
        this.invoker = invoker;
    }
    /**
     * Computes the angle in degrees from the parameter b,
     * Invokes this instance's RotaryInvoker invokeWithDegrees(double) method
     * @see RotaryInvoker
     * @param b  
     */
    public void update(byte[] b) {
        double degrees = getDegrees(b);
        if (inRange(degrees))
            invoker.invokeWithDegrees(degrees);
    }   
    /**
     * Computes the angle in degrees from the byte[] b
     * @param b byte[] read from the rotary sensor
     * @return angle in degrees
     */
    private double getDegrees(byte[] b){
        int[] v = unsign(b);
        double sensorValue = (v[1]*256) + v[2];
        double voltage = sensorValue * ADC_REF / 1023;
        double degrees = voltage * FULL_ANGLE / GROVE_VCC;
        return degrees;
    }
    
    private int[] unsign(byte[] b) {
        int[] v = new int[b.length];
        for (int i = 0; i < b.length; i++) 
            v[i] = unsign(b[i]);
        return v;
    }

    private int unsign(byte b) {
        return b & 0xFF;
    }   
    
    private boolean inRange(double degrees){
        return (0 <= degrees && degrees <= FULL_ANGLE);
    }
}
