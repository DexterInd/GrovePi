use std::io;
use std::{thread, time};

use rppal::i2c;


// device structure for Grove RGB LCD Display
#[derive(Debug)]
pub struct GroveRgbLcd 
{
    i2c: i2c::I2c,
    // row_cursor keeps track of NEXT ROW to be written -- internal state
    //  logic in #write_row will clear/reset the display when next row is 0
    //  the #write_line method will advance to the next row on column wrap 
    //      -OR- on newlines in the input text
    //
    // This means that long inputs will just overwrite and may not be seen
    //  if this behavior is NOT desired, manage input to the LINE_LENGTH
    //  and add delays, etc.
    row_cursor: u8,
}


pub const DISPLAY_RGB_ADDR: u16 = 0x62;
pub const DISPLAY_TEXT_ADDR: u16 = 0x3e;

const PROGRAM_MODE: u8 = 0x80;

const CLEAR_DISPLAY: u8 = 0x01;
const DISPLAY_ON: u8 = 0x08;
const NO_CURSOR: u8 = 0x04;
const ENABLE_2ROWS: u8 = 0x28;

const LINE_LENGTH: usize = 16;

pub const DISPLAY_CHAR: u8 = 0x40;
pub const NEW_ROW: u8 = 0xc0;


impl GroveRgbLcd 
{
    pub fn set_text(&mut self, text: &str) -> Result<(), io::Error>
    {
        match self.impl_set_text(text)
        {
            Err(err) =>  Err(io::Error::new(io::ErrorKind::Other, err)),
            Ok(_) => Ok(())
        }
    }
    pub fn set_rgb(&mut self, (r, g, b): (u8, u8, u8)) -> Result<(), io::Error>
    {
        match self.impl_set_rgb((r, g, b))
        {
            Err(err) =>  Err(io::Error::new(io::ErrorKind::Other, err)),
            Ok(_) => Ok(())
        }
    }
}

impl GroveRgbLcd
{
    fn select_slave(&mut self, addr: u16) -> i2c::Result<()>
    {
        println!("set slave {:x}", addr );
        self.i2c.set_slave_address(addr)
    }

    fn clear_display(&mut self) -> i2c::Result<()>
    {
        println!("set display");
        self.i2c.block_write(PROGRAM_MODE, &[CLEAR_DISPLAY])?;
        thread::sleep(time::Duration::from_millis(50));

        self.row_cursor = 0;

        Ok(())
    }

    fn display_on_no_cursor(&mut self) -> i2c::Result<()>
    {
        self.i2c.block_write(PROGRAM_MODE, &[DISPLAY_ON | NO_CURSOR])
    }

    fn enable_2rows(&mut self) -> i2c::Result<()>
    {
        self.i2c.block_write(PROGRAM_MODE, &[ENABLE_2ROWS])?;
        thread::sleep(time::Duration::from_millis(50));

        Ok(())
    }

    fn new_row(&mut self) -> i2c::Result<()>
    {
        self.i2c.block_write(PROGRAM_MODE, &[NEW_ROW])?;
        self.row_cursor = (self.row_cursor + 1)%2;

        Ok(())
    }

    // writes a row of chars -- no checking for line length or newline
    fn write_row(&mut self, row: &[u8]) -> i2c::Result<()>
    {
        if self.row_cursor == 0 
        {
            self.clear_display()?;
        }
        
        for ch in row
        {
            self.i2c.block_write(DISPLAY_CHAR, &[*ch])?;
        }

        Ok(())
    }
    
    // write_line()
    //  a line has no '\n's in it... but will be wrapped at the display length
    //  and written on two rows
    //  Display is cleared before writing the line
    fn write_line(&mut self, line: &str) -> i2c::Result<()>
    {
        println!("writing line: {}", line) ;

        for row in line.as_bytes().chunks(LINE_LENGTH)
        {
            self.write_row(row)?;
            self.new_row()?;
        }

        Ok(())
    }


    fn impl_set_text(&mut self, text: &str) -> Result<(), i2c::Error>
    {
        self.select_slave(DISPLAY_TEXT_ADDR)?;

        self.clear_display()?;

        self.display_on_no_cursor()?;
        self.enable_2rows()?;

        // spool out text one char at a time
        //  First split on newlines (user formatting) with .lines()
        // then split those lines a line length (wrapped lines) with .chunks()

        println!("ready to write {}", text);
        
        for line in text.lines()
        {
            self.write_line(line)?;
        }

        Ok(())
    }

    fn impl_set_rgb(&mut self, (r, g, b): (u8, u8, u8)) -> Result<(), i2c::Error>
    {
        self.select_slave(DISPLAY_RGB_ADDR)?;

        self.i2c.block_write(0x00, &[0x00])?;
        self.i2c.block_write(0x01, &[0x00])?;
        self.i2c.block_write(0x08, &[0xAA])?;


        self.i2c.block_write(0x04, &[r])?;
        self.i2c.block_write(0x03, &[g])?;
        self.i2c.block_write(0x02, &[b])?;

        Ok(())
    }
}

pub fn connect() -> Result<GroveRgbLcd, io::Error>
{
    println!("connecting I2C bus");

    match i2c::I2c::new()
    {
        Err(err) =>  Err(io::Error::new(io::ErrorKind::Other, err)),
        Ok(i2c) => Ok(GroveRgbLcd{i2c: i2c, row_cursor: 0}),
    }
}

