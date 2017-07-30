# IoTDevices
Grove Pi library

The grovepi for Java8 library is provided as maven projects.

Since you need native access to the raspberry pi device you have 2 choices:
- Use the Pi4J library (third party: http://pi4j.com/)
- Use the DeviceIO library (JDK: http://docs.oracle.com/javame/8.0/api/dio/api/index.html)
You may choose which one to use. If you want to use pi4j then you dont need to add the Device IO libraries. There is no difference in how to use the components, its just a matter of which implementation you want to use to interact with the GPIO ports of the raspberry pi.


## BUILD
run:
mvn install

This creates the .jar files inside the target folder of each of the following projects:
- GrovePi-Spec
- GrovePi-pi4j
- GrovePi-dio

## INCLUDING THE LIBRARIES IN YOUR PROJECTS

Include the GrovePi-Spec jar. This is the core of the library.
Include the implementation you want to use:
- GrovePi-pi4j and the pi4j jar 
 - Install running in the pi: curl -s get.pi4j.com | sudo bash
 - Download the pi4j jar and add it to your project libraries
- GrovePi-dio and the DeviceIO jar
 - Install in the pi and add the resulting jar to your project: https://wiki.openjdk.java.net/display/dio/Getting+Started
 - To run using DIO remember to add: -Djava.library.path="/home/pi/dio/build/so" -Djava.security.policy="/home/pi/dio/dio.policy" to your Java command

Alternatively: Use maven dependencies:

Mandatory:

    <dependency>
      <groupId>org.iot.raspberry</groupId>
      <artifactId>GrovePi-spec</artifactId>
      <version>0.1.0-SNAPSHOT</version>
    </dependency>

Device Implementation:

    <dependency>
      <groupId>org.iot.raspberry</groupId>
      <artifactId>GrovePi-pi4j</artifactId>
      <version>0.1.0-SNAPSHOT</version>
    </dependency>

OR

    <dependency>
      <groupId>org.iot.raspberry</groupId>
      <artifactId>GrovePi-dio</artifactId>
      <version>0.1.0-SNAPSHOT</version>
    </dependency>

Remember to install pi4j or dio.

## RUNNING THE EXAMPLES

Examples are provided as a simple netbeans project, this is done to facilitate running it using the remote JVM feature: http://blog.weston-fl.com/configure-netbeans-to-test-and-deploy-raspberry-pi-project/

To run the project provide two parameters:
- the implementation: pi4j or dio
- the class to run: 

You may build the project and copy the examples.jar, GrovePi-spec.jar, GrovePi-pi4j.jar, GrovePi-dio.jar, ( pi4j.jar and/or deviceIo.jar )
Then run the examples using all the jars as classpath and the main class: org.iot.raspberry.examples.Runner
Ex. java -cp lib/* org.iot.raspberry.examples.Runner pi4j BlinkingLed

All the examples contains instructions on how to connect the devices to the grovepi board.

To stop the examples (for those that run eternally)
- If running directly in the pi enter quit in the console.
- If running remotely using netbeans: run the project again. (first time you run it, starts the project, second time it stops it. (useful since you dont have a console to type to))

## STARTING YOUR OWN PROJECT

If using maven use the dependencies above otherwise add the jars to your project.

Alternatively you may copy all the classes in the GrovePi-Spec project and the deviceIo or Pi4J classes to a new project. (if you want a single jar). Be warned that you still need the pi4j or deviceIO libraries.

## USAGE

Simply create a new instance of the GrovePi class with the implementation you want:

GrovePi grovepi = new GrovePi4J();
OR
GrovePi grovepi = new GrovePiDio();

Then create the connected devices and provide the grovepi you created as parameter in constructors:

GroveTemperatureAndHumiditySensor dht = new GroveTemperatureAndHumiditySensor(grovePi, 4, GroveTemperatureAndHumiditySensor.Type.DHT11)

Or for simple digital in or out use
GroveDigitalOut led = grovePi.getDigitalOut(4);

The number in the parameters is usually the port number you are using.

*NOTE* YOU MUST NOT CREATE MULTIPLE GrovePi objects! use the same for all the devices connected to your board. using multiple may cause collisions in device access.
