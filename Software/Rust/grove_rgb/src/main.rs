use std::error::Error;
use std::{thread, time};

mod grove_rgb_lcd;


fn main() -> Result<(), Box<dyn Error>> {
    println!("Hello, LCD");

    let mut display: grove_rgb_lcd::GroveRgbLcd = grove_rgb_lcd::connect()?;
    println!("{:?}", display);

    display.set_rgb((0x80, 0x00, 0x00))?;  // red
    display.set_text("FUBAR!\n@@snafu\nline1\nline2\n0123456789ABCDEF0123456789abcdef")?;
    thread::sleep(time::Duration::from_millis(5000));

    display.set_rgb((0x20, 0xA0, 0x40))?;
    display.set_text("dunno what color this is")?;
    thread::sleep(time::Duration::from_millis(5000));

    display.set_rgb((0x00, 0x40, 0xFF))?;
    display.set_text("now i'm bright BLUE - like my ballz!")?;
    thread::sleep(time::Duration::from_millis(5000));

    Ok(())
}
