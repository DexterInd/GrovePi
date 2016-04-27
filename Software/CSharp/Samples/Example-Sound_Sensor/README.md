## **Sound Sensor Example**
This sample will demonstrate how to use the [Grove Sound Sensor](http://www.dexterindustries.com/shop/grove-sound-sensor/) with the GrovePi and Raspberry Pi. This sample is designed to run on a Raspberry Pi 2 running Windows 10 IoT Core. The application is written as a Background Task and will run in Windows 10 IoT Core without any user interface.

### Requirements
You must have the following:

- [Windows 10](https://www.microsoft.com/windows/)
- [Visual Studio 2015 Community Edition](https://www.visualstudio.com/) or better
- [Raspberry Pi 2 running Windows 10 IoT Core](http://ms-iot.github.io/content/en-US/win10/RPI.htm)
- [GrovePi+ Starter Kit for Raspberry Pi](http://www.dexterindustries.com/grovepi-starter-kit/)

### Install a Visual Studio 2015
If you don't already have one installed, install Visual Studio 2015. You can use the free Community edition, or any other higher edition. When you are installing Visual Studio, you must do a __Custom__ install and select to install the __Universal Windows App Development Tools -> Tools and Windows SDK__. 

After the installation is complete, install the Windows IoT Core Project Templates from [here](https://visualstudiogallery.msdn.microsoft.com/55b357e1-a533-43ad-82a5-a88ac4b01dec).

### Enable Developer Mode on your Windows 10 Development Device
When you are developing on Windows 10, you choose what tasks you want to enable on the device. This includes any devices - Windows 10 desktops, tablets and phones. You can enable a device for development, or just app side loading. To enable _Developer mode_ on your Windows 10 device:

1. Click the Windows icon (typically in the lower-left of the screen, on the left-most side of the toolbar). 
2. Type __Update__ and select _Windows Update settings_ from the _Best match_ list. This will open the __UPDATE & SECURITY__ settings page. 
3. Click on __For developers__ in the left sidebar.
4. Ensure the __Developer mode__ radio button is selected.
5. Save your changes and close the _Settings_ window.  

### Build the Samples
Download the GrovePi repository to your development PC.

Each sample is its own solution. There are two ways to run the sample projects - within the GrovePi solution, or as individual solutions.

#### Samples as Part of GrovePi solution (recommended)
When you run the samples as part of the GrovePi solution you know that you are using the very latest build of GrovePi, however; the samples are not part of the GrovePi solution by default - you must add them.

1. Open __GrovePi\Software\CSharp\GrovePi.sln__ in Visual Studio
2. Right-click on the solution in the _Solution Explorer_
3. Select __Add__ > __ New Solution Folder__
4. Name the folder __Samples__
5. Right-click on the solution in the _Solution Explorer_
6. Select __Add__ > __ Existing Project__
7. Find the __SoundSensor.csproj__ file - select it and click __Open__

This will add the _SoundSensor_ project to you new _Samples_ directory.

In the _SoundSensor_ project you need to update the reference to _GrovePi_.

1. In _Solution Explorer_ expand the _SoundSensor_ project and the _References_ node.
2. Right-click on the __GrovePi__ reference and click __Remove_
3. Right-click on the __References__ node and choose __Add Reference__
4. Expand the __Projects__ node
5. Select (by checking the check box) the __GrovePi__ project.
6. Click __OK__

The project should now have all the updated references you need. 

#### Samples as Independent Solutions
When you run the sampels as independent solutions, you need to ensure you are referencing a current version of the GrovePi assembly (likely more current than the one available as a NuGet package). 

The following steps assume you have already opened _GrovePi\Software\CSharp\GrovePi.sln_ in Visual Studio and built the solution.  To build the solution, open GrovePi.sln, and click on press CTRL + SHIFT + B.  Then close GrovePi.sln.

After building the GrovePi solution:   

1. Open __GrovePi\Software\CSharp\Samples\SoundSensor.sln__ in Visual Studio.   
2. In _Solution Explorer_ expand the _SoundSensor_ project and the _References_ node.  
3. Right-click on the __GrovePi__ reference and click __Remove_.  
4. Right-click on "References" and click "Add Reference".  
5. Select the __Browse__ tab and click the __Browse__ button.  
6. Browse to __GrovePi\Software\CSharp\GrovePi\bin\ARM\Debug__ and select the __GrovePi.dll__ file  
7. Click __OK__  

The project should now have all the updated references you need. 

### Setup the Hardware
For this sample, connect the following:

1. Sound Sensor to __A0__ (Analog Pin 0)


### Run the Sample
To run the sample... 

1. Right-click on the _SoundSensor_ project in the _Solution Explorer_
2. Select __Set as Startup Project__
3. Right-click on the __Properties__ node under _SoundSensor_ and select __Open__
4. Select the __Debug__ tab
5. Select __Remote Machine__ in the _Target device_ field
6. In the __Remote Machine__ field, Type in the name or IP Address of your Windows 10 IoT Core Raspberry Pi
7. Press __Ctrl__ + __S__ (this file will not be saved automatically, you must save it manually).
8. Press __F5__ to launch the debugger (it will take a minute or two to deploy your app onto the Raspberry Pi).
