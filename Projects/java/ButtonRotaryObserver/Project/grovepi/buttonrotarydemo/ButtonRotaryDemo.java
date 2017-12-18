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
 * GrovePi for the Raspberry Pi: an open source platform for connecting Grove 
 * Sensors to the Raspberry Pi.
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


import grovepi.observer.ButtonInvoker;
import grovepi.observer.ButtonPressDistinguisher;
import grovepi.observer.DigitalInputReader;

import grovepi.observer.RotaryInvoker;
import grovepi.observer.RotaryAngleDeterminer;
import grovepi.observer.AnalogInputReader;



/**
 * ButtonRotaryDemo
 * This GrovePi sensor demonstration is part of a coursework project
 * for CS505 Design Patterns, at Central Connecticut State University,
 * Fall 2017, with Dr. Chad Williams.
 * 
 * The main method creates a BottonInvoker object and begins listening for button events:
 * singlePress, doublePress, and longPress. Each of these events will invoke methods
 * implemented in SampleButtonInvoker. Write your own class that implements ButtonInvoker interface.
 * (SampleButtonInvoker is quite boring)
 * 
 * @see SampleButtonInvoker
 * @see grovepi.observer.ButtonInvoker
 * 
 * The main method also creates a RotaryInvoker object and begins reading the
 * angle of the rotary sensor. Each time the angle is read, the method 
 * invokeWithDegrees(degrees) of SampleRotaryInvoker is executed.  Write your own class that 
 * implements RotaryInvoker interface. (SampleRotaryInvoker is even more boring)
 * 
 * @see SampleRotaryInvoker
 * @see grovepi.observer.RotaryInvoker
 * 
 * @author James Luczynski
 * @author Jeff Blankenship
 */
public class ButtonRotaryDemo{    
    /**
     * @param args the command line arguments
     * @throws java.lang.InterruptedException
     * @throws java.lang.Exception
     */
    public static void main(String[] args){
      
        //button can be connected to D2-D8.
        int buttonPin = 6; 
        //rotary can be connected to A0, A1, A2
        int rotaryPin = 2;

        //instantiate a ButtonInvoker
        SampleButtonInvoker invoker = new SampleButtonInvoker();  
        initButton(invoker, buttonPin);
        
        //instantiate a RotaryInvoker
        SampleRotaryInvoker rotaryInvoker = new SampleRotaryInvoker();
        initRotary(rotaryInvoker,rotaryPin);        
    }
    /**
     * Initializes DigitalInputReader and ButtonPressDistinguisher objects.
     * Button presses will invoke the methods defined in the ButtonInvoker parameter.
     * @param invoker any object of a class that implements ButtonInvoker interface
     * @param pin the GrovePi port number the button sensor is plugged into
     */
    public static void initButton(ButtonInvoker invoker, int pin) {
        try {
            DigitalInputReader buttonReader = new DigitalInputReader(pin);
            ButtonPressDistinguisher distinguisher = new ButtonPressDistinguisher(invoker);
            buttonReader.addObserver(distinguisher);
            buttonReader.startReading();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    /**
     * Initializes AnalogInputReader and RotaryAngleDeterminer objects.
     * Rotations of the rotary sensor will invoke the method defined in the RotaryInvoker parameter.
     * @param invoker any object of a class that implements RotaryInvoker interface
     * @param pin the GrovePi port number the rotary sensor is plugged into
     */
    public static void initRotary(RotaryInvoker invoker, int pin){
        try {
            AnalogInputReader rotaryReader = new AnalogInputReader(pin);
            RotaryAngleDeterminer determiner = new RotaryAngleDeterminer(invoker);
            rotaryReader.addObserver(determiner);
            rotaryReader.startReading();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
