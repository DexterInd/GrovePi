package grovepi.buttonrotarydemo;

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
import grovepi.observer.RotaryInvoker;
import java.text.DecimalFormat;
/**
 * This GrovePi sensor demonstration is part of a coursework project
 * for CS505 Design Patterns, at Central Connecticut State University,
 * Fall 2017, with Dr. Chad Williams.
 * 
 * This class provides a sample implementation of the RotaryInvoker interface.
 * 
 * You can write your own class that implements RotaryInvoker interface (this one is very boring)
 * to determine what happens on based on the angle of the rotary sensor.
 * 
 * @see grovepi.observer.ButtonInvoker
 * @author James Luczynski
 * @author Jeff Blankenship
 */
public class SampleRotaryInvoker implements RotaryInvoker{
    /**
     * Angle from the previous reading of the rotary sensor.
     * NOTE: the rotary sensor has only 300 degrees of rotation.
     */
    private double degrees;
    /**
     * A somewhat arbitrary number. If the difference in degrees from the previous
     * reading and the most recent reading is less than the tolerance, don't do anything.
     */
    private double tolerance = 4;
    /**
     * Prints current angle of rotary sensor if different from last reading
     * @param degrees most recent reading of rotary sensor angle
     */
    public void invokeWithDegrees(double degrees){
        if (Math.abs(this.degrees - degrees) > tolerance)     
        {
            this.degrees = degrees;
            DecimalFormat df = new DecimalFormat("###.#");
            String output = df.format(this.degrees);
            System.out.println("Rotary sensor position (degrees): " + output);
        }
    }
}