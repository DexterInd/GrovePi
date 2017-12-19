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
 * An instance of this class recieves updates containing sensor events, analyzes 
 * the timing of these events and invokes the appropriate method on this instance's
 * ButtonInvoker object.  The ButtonInvoker object can be changed at runtime
 * to get different behaviour triggered by button presses.
 * 
 * @see ButtonInvoker
 * @author James Luczynski
 * @author Jeff Blankenship
 */
public class ButtonPressDistinguisher implements InputSensorObserver, Runnable{

    private boolean buttonDown = false;
    private boolean waitingForSecondPress = false;
    private long lastPress;
    private long lastRelease;
    private Thread thread = new Thread(this);
    private int longPressTimeInterval = 1000;
    private int doublePressTimeInterval = 1000;
    private ButtonInvoker invoker;
    
    /**
     * Constructor
     * @see ButtonInvoker
     * @param invoker 
     */
    public ButtonPressDistinguisher(ButtonInvoker invoker){
        this.invoker = invoker;
    }    
    /**
     * Changes this instance's buttonInvoker object to the one in the argument provided.
     * @param invoker 
     */
    public void setInvoker(ButtonInvoker invoker){
        this.invoker = invoker;
    }    
    /**
     * Analyzes the timing of button events and determines if a single, double or long press
     * has occurred. It then invokes the associated method on this instance's ButtonInvoker object
     * @param b the byte[] read from the button sensor
     */
    public void update(byte[] b){  
        long timeOfAction = System.currentTimeMillis();
        buttonDown = b[0] == 1 ? true : false;
        if (buttonDown) {                   //if this update results from button being pressed down.
            lastPress = timeOfAction;
        } else{                             //button was just released
            lastRelease = timeOfAction;           
            if (lastRelease - lastPress > longPressTimeInterval){
                invoker.longPress();                
            }
            else{
                if (thread.isAlive()){ //if thread still waiting, it's a double press    
                    invoker.doublePress();
                    waitingForSecondPress = false;
                }else{ //this press is not second press of a double press, must wait
                    waitingForSecondPress = true;
                    thread = new Thread(this);
                    thread.start();
                }                    
            }
        }   
    }    
    
    public void run(){
        try{
            Thread.sleep(doublePressTimeInterval);  //after "enough" time has elapsed,
            if(waitingForSecondPress){              //and still waiting for second press, then it's a single press
                invoker.singlePress();
                waitingForSecondPress = false;
            }                
        }catch (InterruptedException e){
            e.printStackTrace();
        }
    }    
    /**
     * Changes the time interval that two button presses must occur within, in 
     * in order to be considered a double press
     * @param interval the new double press interval in milliseconds
     */
    public void setDoublePressInterval(int interval){
        doublePressTimeInterval = interval;
    }    
    /**
     * @return the current double press time interval in milliseconds
     */
    public int getDoublePressInterval(){
        return doublePressTimeInterval;
    }
    /**
     * Changes the length of time (in milliseconds) that the button must be 
     * continuously pressed down for in order for that press to be considered a long press
     * @param interval the new long press interval in milliseconds
     */
    public void setLongPressInterval(int interval){
        longPressTimeInterval = interval;
    }
    /**
     * @return the current long press time interval in milliseconds.
     */
    public int getLongPressInterval(){
        return longPressTimeInterval;
    }   
}
