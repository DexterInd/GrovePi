package grovepiDHT

import (
	"sync"
	"time"
	"unsafe"

	"github.com/TIBCOSoftware/flogo-lib/core/activity"
	"github.com/TIBCOSoftware/flogo-lib/logger"
	"github.com/mrmorphic/hwio"
)

// log is the default package logger
var log = logger.GetLogger("activity-tibco-GrovePiDHT")

const (
	ivPin         = "pin"
	ovTemperature = "temperature"
	ovHumidity    = "humidity"

	//Cmd format
	DHT_READ = 40
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

	log.Debug("Starting Pin DHT read")
	if context.GetInput(ivPin) != nil {
		pin = byte(context.GetInput(ivPin).(int))
	}

	var g *GrovePi
	g = InitGrovePi(0x04)
	defer g.CloseDevice()

	t, h, err := g.ReadDHT(pin)
	if err != nil {
		log.Error("GrovePi ReadDHT Issue: ", err)
	}

	context.SetOutput(ovTemperature, t)
	context.SetOutput(ovHumidity, h)

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

func (grovePi *GrovePi) ReadDHT(pin byte) (float32, float32, error) {
	b := []byte{DHT_READ, pin, 0, 0}
	rawdata, err := grovePi.readDHTRawData(b)
	if err != nil {
		return 0, 0, err
	}
	temperatureData := rawdata[1:5]

	tInt := int32(temperatureData[0]) | int32(temperatureData[1])<<8 | int32(temperatureData[2])<<16 | int32(temperatureData[3])<<24
	t := (*(*float32)(unsafe.Pointer(&tInt)))

	humidityData := rawdata[5:9]
	humInt := int32(humidityData[0]) | int32(humidityData[1])<<8 | int32(humidityData[2])<<16 | int32(humidityData[3])<<24
	h := (*(*float32)(unsafe.Pointer(&humInt)))
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
	raw, err := grovePi.i2cDevice.Read(1, 9)
	if err != nil {
		return nil, err
	}
	return raw, nil
}
