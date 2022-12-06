# Rust support for GrovePi

## Introduction
Rust Crate support for using GrovePi with Rust.

Examples can be found in the relevant directories as `main.rs`.
Check them out for usage.

## Dependencies
* Rust version above 1.65 is known to work.
* The Rust crate [**rppal**](https://github.com/golemparts/rppal) is required and is referenced in the `Cargo.toml` file.

## Current State
As the initial state of this module the following features are implemented and tested:

* Read/write data to I2C slave device [**Grove-LCD RGB Backlight**](https://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/) V. 4.0 present on ports I2C-1, I2C-2 or I2C-3.
* Tested on Raspberry Pi 3, Model B and Raspberry Pi, Model B, Rev 2
  with Raspbian version: September 2022

## Cross compile for Rasbperry Pi

Follow the setup instructions from - (https://github.com/cross-rs/cross)

Then `cross build --target arm-unknown-linux-gnueabi`.  A pi-ready 
and transfer the binary (`target/arm-unknown-linux-gnueabi/debug/airq`) to the Pi.

Run the binary `grove_rgb_lcd` on the Pi and observe a couple debug messages and changing colors.

## Add the module `grove_rgb_lcd` to your projects

Be sure to add the `rppal` dependency to your `Cargo.toml`

