# GrovePi Minecraft Controller
# This is a custom controller for Minecraft, made using the GrovePi.
# In this example, we show you how to build your own custom Minecraft controller
# with the GrovePi.
# See more about the GrovePi at http://dexterindustries.com/grovepi
# A great reference we used is the MagPi's Essentials Minecraft Guide: https://www.raspberrypi.org/magpi-issues/Essentials_Minecraft_v1.pdf
'''
Software Setup:
  Before we begin, run the following commands to setup:
    sudo apt-get install minecraft-pi 
    sudo pip3 install python3-xlib
    sudo pip3 install pyautogui

Hardware Setup:
  Setup the GrovePi on the Raspberry Pi.
  Connect a touch Sensor to port A0.
  Connect a Joystick to port A2.
  Connect a touch sensor to Port D3.
  Connect a touch sensor to Port D4.

To run:
  1.  Start Minecraft on the Pi.
  2.  Start a world.
  3.  Start Python3 (IDLE).
  4.  Open this file (GrovePi-Controller.py)
  5.  Click "Run" --> "Run Module"
  6.  Click back into Minecraft.
'''

import mcpi.minecraft as minecraft
import grovepi
import time
import mcpi.block as block
import pyautogui as pag

# Setup the four sensors.
touch_sensor1 = 4   # This will be the Build Key
touch_sensor2 = 3   # This will be the Destroy Key
touch_sensor3 = 14  # This will be the Fly Key.

# This will be the joystick.
xPin = 16  # Port A2
yPin = 17  # Port A2

grovepi.pinMode(xPin, "INPUT")
grovepi.pinMode(yPin, "INPUT")

grovepi.pinMode(touch_sensor1, "INPUT")
grovepi.pinMode(touch_sensor2, "INPUT")
grovepi.pinMode(touch_sensor3, "INPUT")

flying = 0;

# Creat a minecraft entity.  We'll reference this through the entire program.
mc = minecraft.Minecraft.create()

# unpress() - This function unpresses all keys.
def unpress():
  for key in ['s','w','a','d',' ']:
    pag.keyUp(key)

# move() - This function presses the key "direction"
def move(direction):
  unpress()
  pag.keyDown(direction)

#build - This function builds a square block of "size" size.  
def build(p):
  size = 5
  mc.setBlocks(p.x+1, p.y+1, p.z+1, (p.x + size), (p.y + size), (p.z + size), block.STONE.id)
  print("Build!")

#destroy - This function destroys a square block of "size" size.
def destroy(p):
  size = 5
  mc.setBlocks(p.x+1, p.y+1, p.z+1, (p.x + size), (p.y + size), (p.z + size), block.AIR.id)
  print("Destroy!")

# fly - This starts and stops the flying mode.
def fly():
  pag.keyDown(' ')
  pag.keyUp(' ')
  pag.keyDown(' ')
  pag.keyUp(' ')
  print("Flying!")

# We do the following loop over and over.
while True:

  p = mc.player.getTilePos()    # Get the position of our person in Minecraft.

  try:

    # Read the three keys.
    # Touch Sensor 1:  Build something if it's touched.
    if(grovepi.digitalRead(touch_sensor1)):
      build(p)                                       
    # Touch Sensor 2:  Destroy something if it's touched.
    if(grovepi.digitalRead(touch_sensor2)):
      destroy(p)
    # Touch Sensor 3:  Start or stop flying if it's been touched.
    if(grovepi.digitalRead(touch_sensor3)):
      #The variable flying is whether we're flying or not.
      if(flying == 0):
        flying = 1
        fly()
      else:
        flying = 0

      
    # Read the joystick.  We do that with the two pins x and y.
    x = grovepi.analogRead(xPin)
    y = grovepi.analogRead(yPin)

    # Check to see if the joystick has been pressed down. 
    click = 1 if x >= 1020 else 0
    print(str(x) + ", " + str(y))
    
    # Check to see if we've been put into flying mode.  If we have, we can teleport ourselves!
    if(flying):
      jump = 5   # This is the jump size, how far we're going to jump in each direction.
      playerPosition = mc.player.getPos()       # Get our persons position in Minecraft.

      # Now we'll take the joystick values and jump in the direction it tells us to.
      if(x < 400):
        mc.player.setPos(playerPosition.x+jump, playerPosition.y, playerPosition.z)

      # Here we will make sure that the click and the x-axis reading are not confused.  
      elif(x > 600 and (click == 0)):
        mc.player.setPos(playerPosition.x-jump, playerPosition.y, playerPosition.z)

      elif(y > 600):
        mc.player.setPos(playerPosition.x, playerPosition.y+jump, playerPosition.z)

      elif(y < 400):
                  mc.player.setPos(playerPosition.x, playerPosition.y-jump, playerPosition.z)

      # If we didn't read anything, unpress the buttons.  
      else:
        unpress()

    # If the joystick is clicked, we fly up one spot.  
    if(click):
      pag.keyUp(' ')
      pag.keyDown(' ')
      

  except IOError:
    print("Error")

