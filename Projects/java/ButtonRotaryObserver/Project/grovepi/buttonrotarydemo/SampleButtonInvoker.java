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

import grovepi.observer.ButtonInvoker;

/**
 * ButtonInvoker Sample.
 * This GrovePi sensor demonstration is part of a coursework project
 * for CS505 Design Patterns, at Central Connecticut State University,
 * Fall 2017, with Dr. Chad Williams.
 * 
 * ButtonInvokerdemo realizes the ButtonInvoker interface and provides
 * a sample implementation for each of its methods. 
 * 
 * You can write your own class that implements ButtonInvoker interface (this one is very boring)
 * to determine what happens for each different press
 * 
 * @see grovepi.observer.ButtonInvoker
 * @author James Luczynski
 * @author Jeff Blankenship
 */
public class SampleButtonInvoker implements ButtonInvoker{
    

    @Override
    public void singlePress(){
        //singlePress code
        System.out.println("Single Press");
    }
    

    @Override
    public void doublePress(){
        //doublePress code
        System.out.println("Double Press");
    }
    

    @Override
    public void longPress(){
        //longPress code
        System.out.println("Long Press");
    }
}
