

### GrovePi sensors implemented using Java

This project is an example of how GrovePi libraries can be used in a Java application which interacts with GrovePi sensors, specifically the button and rotary used in this project.  The GrovePi.observer package has been written in a way to provide a framework where these classes can be extended to use other sensors as needed.

### ButtonRotaryDemo
ButtonRotaryDemo provides an example of a client class interacting with the observer package.  

For each button or rotary sensor that is desired, the developer must implement an invoker interface (either implements ButtonInvoker or implements RotaryInvoker).  Within the newly created class include the code for the action desired for any of the button/rotary events.

Invokers
 * **SamplebuttonInvoker**: Provides specific code to be executed when a single, double, or long press is invoked.  In this example it simply prints a message to the console.
 * **SampleRotaryInvoker**: Provides code to be executed when a change is detected in the position of the rotary sensor.  In this example a filter is applied such that minimum difference of SampleRotaryInvoker.tolerance is required to trigger a display.  Also, the output is formatted for single decimal place display.

Once an invoker is implemented, the next step is to code a driver that uses the invoker.  In this example, 
**ButtonRotaryDemo.java**: Instantiates invokers, assigns invokers to sensors and pins and starts reading the sensors. 

### Deploying to your machine
This project was devoloped using NetBeans IDE 8.2.  Only the java files have been included in the repository to allow users to compile them as projects in any developement environment.

Specifically for NetBeans, the process to create and run this as a project is as follows:
1. Clone a local copy of the repository.
2. Create a new project in NetBeans: File-> New Project, Java, Java Application.
3. Within the "Source Packages" folder of the newly created project, copy the folders 
~\GrovePi\Projects\java\ButtonRotaryObserver\Project\grovepi\buttonrotarydemo
~\GrovePi\Projects\java\ButtonRotaryObserver\Project\grovepi\observer
4. The project uses the other GrovePi packages through jar files.  The NetBeans project must be pointed to the correct jar files.

   a. Right click the project name and select "Properties".
   
   b. In the Categories tree on the lest, select "Libraries".
   
   c. Click "Add JAR/Folder"
   
   d. Navigate to ~\GrovePi\Projects\java\ButtonRotaryObserver\Project\grovepi\observer and select each of the  jar files there, grovepi.jar and pi4j.jar.   *Note: This step must be repeated after moving the project to a different platform (ie moving it to the pi) due to different file structures.*
   
   e. Click OK to accept changes.
  
5. Run the file ButtonRotaryDemo. 



### Package grovepi.observer

This package provides the tools used to create the invokers.  
* **InputSensorReader**: Provides a common set of control methods and class variables for subclasses.

  * **DigitalInputReader (extends InputSensorReader)**: Reads sensor data from a GrovePi digital sensor and updates an observer with this data.

  * **AnalogInputReader (extends InputSensorReader)**:  An instance of this class reads sensor data from a GrovePi analog sensor and updates an observer with this data.

* **InputSensorObserver**: Provides the interface that all concrete InputSensorObservers must implement.

  * **ButtonPressDistinguisher (implements InputSensorObserver)**: Receives updates containing sensor events, analyzes the timing of these events and invokes the appropriate method on this instance's ButtonInvoker object.

  * **RotaryAngleDeterminer (implements InputSensorObserver)**: Determines and reports the angular position of the rotary angle sensor.  
  
* **Interfaces**:
  * **ButtonInvoker**: Declares the methods that are called when ButtonPressDistinguisher identifies a single, double, and long press respectively.
  * **RotaryInvoker**: Declares a method to call when RotaryAngleDenterminer is updated.
  
This package uses the Observer design pattern, and can be used to easily incorporate other input sensors into your project.  Simply write a class that implements the InputSensorObserver interface and includes a way of processing the data read from the sensor. 
### Credits

This GrovePi sensor demonstration is an extension of coursework for CS505 Design Patterns at Central Connecticut State University,
Fall 2017, with Dr. Chad Williams.  

Interested in Computer Science at CCSU?:  http://www.ccsu.edu/cs/

@author James Luczynski

@author Jeff Blankenship

## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017 Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
