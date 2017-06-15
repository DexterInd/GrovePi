package grovepi

import (
	"encoding/binary"
	"math"
	"time"

	"github.com/mrmorphic/hwio"
)

// Pins
const (
	A0 = 0
	A1 = 1
	A2 = 2

	D2 = 2
	D3 = 3
	D4 = 4
	D5 = 5
	D6 = 6
	D7 = 7
	D8 = 8
)

// Commands format
const (
	CommandDigitalRead  = 1
	CommandDigitalWrite = 2
	CommandAnalogRead   = 3
	CommandAnalogWrite  = 4
	CommandPinMode      = 5
	CommandDHTRead      = 40
)

// PinMode determines the pinmode for the GrovePi
type PinMode byte

// InputPin is the pinmode for input
// OutputPin is the pinmode for output
const (
	InputPin  PinMode = 0
	OutputPin         = 1
)

// GrovePi struct is used for handling the connection with board
type GrovePi struct {
	i2cmodule hwio.I2CModule
	i2cDevice hwio.I2CDevice
}

// Init initializes the GrovePi
func Init(address int) (*GrovePi, error) {
	grovePi := new(GrovePi)
	m, err := hwio.GetModule("i2c")
	if err != nil {
		return nil, err
	}

	grovePi.i2cmodule = m.(hwio.I2CModule)
	err = grovePi.i2cmodule.Enable()
	if err != nil {
		return nil, err
	}

	grovePi.i2cDevice = grovePi.i2cmodule.GetDevice(address)
	return grovePi, nil
}

// Close closes the connection with the GrovePi
func (grovePi *GrovePi) Close() {
	grovePi.i2cmodule.Disable()
	hwio.CloseAll()
}

// AnalogRead reads analogically to the GrovePi
func (grovePi *GrovePi) AnalogRead(pin byte) (int, error) {
	b := []byte{CommandAnalogRead, pin, 0, 0}
	err := grovePi.i2cDevice.Write(1, b)
	if err != nil {
		return 0, err
	}
	time.Sleep(100 * time.Millisecond)

	grovePi.i2cDevice.ReadByte(1)
	val, err := grovePi.i2cDevice.Read(1, 4)
	if err != nil {
		return 0, err
	}

	return ((int(val[1]) << 8) | int(val[2])), nil
}

// DigitalRead reads digitally to the GrovePi
func (grovePi *GrovePi) DigitalRead(pin byte) (byte, error) {
	b := []byte{CommandDigitalRead, pin, 0, 0}
	err := grovePi.i2cDevice.Write(1, b)
	if err != nil {
		return 0, err
	}
	time.Sleep(100 * time.Millisecond)

	return grovePi.i2cDevice.ReadByte(1)
}

// DigitalWrite writes digitally to the GrovePi
func (grovePi *GrovePi) DigitalWrite(pin byte, val byte) error {
	b := []byte{CommandDigitalWrite, pin, val, 0}
	err := grovePi.i2cDevice.Write(1, b)
	time.Sleep(100 * time.Millisecond)
	return err
}

// PinMode sets the GrovePi pinmode
func (grovePi *GrovePi) PinMode(pin byte, mode PinMode) error {
	b := []byte{CommandPinMode, pin, byte(mode), 0}

	err := grovePi.i2cDevice.Write(1, b)
	time.Sleep(100 * time.Millisecond)
	return err
}

// ReadDHT returns temperature and humidity from DHT sensor
func (grovePi *GrovePi) ReadDHT(pin byte) (float32, float32, error) {
	b := []byte{CommandDHTRead, pin, 0, 0}
	rawdata, err := grovePi.readDHTRawData(b)
	if err != nil {
		return 0, 0, err
	}

	temperatureData := binary.LittleEndian.Uint32(rawdata[1:5])
	t := math.Float32frombits(temperatureData)

	humidityData := binary.LittleEndian.Uint32(rawdata[5:9])
	h := math.Float32frombits(humidityData)

	return t, h, nil
}

func (grovePi *GrovePi) readDHTRawData(cmd []byte) ([]byte, error) {
	err := grovePi.i2cDevice.Write(1, cmd)
	if err != nil {
		return nil, err
	}
	time.Sleep(600 * time.Millisecond)
	grovePi.i2cDevice.ReadByte(1)
	time.Sleep(100 * time.Millisecond)

	return grovePi.i2cDevice.Read(1, 9)
}
