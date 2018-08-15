package grovepiDigitalWrite

import (
	"sync"
	"time"

	"github.com/TIBCOSoftware/flogo-lib/core/activity"
	"github.com/TIBCOSoftware/flogo-lib/logger"
	"github.com/mrmorphic/hwio"
)

// log is the default package logger
var log = logger.GetLogger("activity-tibco-GrovePi")

const (
	ivPin     = "pin"
	ivValue   = "value"
	ovSuccess = "success"

	//Cmd format
	DIGITAL_WRITE = 2
	PIN_MODE      = 5
)

type GrovePi struct {
	i2cmodule hwio.I2CModule
	i2cDevice hwio.I2CDevice
}

// Activity is a Activity implementation
type grovePiDWActivity struct {
	sync.Mutex
	metadata *activity.Metadata
}

// NewActivity creates a new Activity
func NewActivity(metadata *activity.Metadata) activity.Activity {
	return &grovePiDWActivity{metadata: metadata}
}

// Metadata implements activity.Activity.Metadata
func (a *grovePiDWActivity) Metadata() *activity.Metadata {
	return a.metadata
}

// Eval implements activity.Activity.Eval
func (a *grovePiDWActivity) Eval(context activity.Context) (done bool, err error) {

	var pin byte
	var value bool

	log.Debug("Starting Pin Write")
	if context.GetInput(ivPin) != nil {
		pin = byte(context.GetInput(ivPin).(int))
	}
	if context.GetInput(ivValue) != nil {
		value = context.GetInput(ivValue).(bool)
	}

	var g *GrovePi
	g = InitGrovePi(0x04)
	err = g.PinMode(pin, "output")
	if err != nil {
		log.Error("GrovePi :: Set PinMode Error", err)
	}

	//write to GrovePi
	if value {
		g.DigitalWrite(pin, 1)
	} else {
		g.DigitalWrite(pin, 0)
	}

	context.SetOutput(ovSuccess, true)

	return true, nil
}

func InitGrovePi(address int) *GrovePi {
	grovePi := new(GrovePi)
	m, err := hwio.GetModule("i2c")
	if err != nil {
		log.Error("GrovePi :: could not get i2c module Error", err)
		//fmt.Printf("could not get i2c module: %s\n", err)
		return nil
	}
	grovePi.i2cmodule = m.(hwio.I2CModule)
	grovePi.i2cmodule.Enable()

	grovePi.i2cDevice = grovePi.i2cmodule.GetDevice(address)
	return grovePi
}

func (grovePi GrovePi) CloseDevice() {
	grovePi.i2cmodule.Disable()
}

func (grovePi GrovePi) DigitalWrite(pin byte, val byte) error {
	b := []byte{DIGITAL_WRITE, pin, val, 0}
	err := grovePi.i2cDevice.Write(1, b)
	if err != nil {
		log.Error("GrovePi :: DigitalWrite Error", err)
		return err
	}
	time.Sleep(100 * time.Millisecond)
	return nil
}

func (grovePi GrovePi) PinMode(pin byte, mode string) error {
	var b []byte
	if mode == "output" {
		b = []byte{PIN_MODE, pin, 1, 0}
	} else {
		b = []byte{PIN_MODE, pin, 0, 0}
	}
	err := grovePi.i2cDevice.Write(1, b)
	if err != nil {
		log.Error("GrovePi :: i2cDevice.Write Error", err)
		return err
	}
	time.Sleep(100 * time.Millisecond)
	return nil
}
