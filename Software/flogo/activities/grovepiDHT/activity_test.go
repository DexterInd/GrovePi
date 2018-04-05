package grovepiDHT

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"

	"io/ioutil"

	"github.com/TIBCOSoftware/flogo-contrib/action/flow/test"
	"github.com/TIBCOSoftware/flogo-lib/core/activity"
)

var activityMetadata *activity.Metadata

func getActivityMetadata() *activity.Metadata {

	if activityMetadata == nil {
		jsonMetadataBytes, err := ioutil.ReadFile("activity.json")
		if err != nil {
			panic("No Json Metadata found for activity.json path")
		}

		activityMetadata = activity.NewMetadata(string(jsonMetadataBytes))
	}

	return activityMetadata
}

func TestCreate(t *testing.T) {

	act := NewActivity(getActivityMetadata())

	if act == nil {
		t.Error("Activity Not Created")
		t.Fail()
		return
	}
}

func TestGrovePiDHT(t *testing.T) {

	defer func() {
		if r := recover(); r != nil {
			t.Failed()
			t.Errorf("panic during execution: %v", r)
		}
	}()

	act := NewActivity(getActivityMetadata())
	tc := test.NewTestActivityContext(getActivityMetadata())

	//setup attrs GrovePi Tester, using Pin 4
	tc.SetInput(ivPin, 4)

	act.Eval(tc)

	temp := tc.GetOutput(ovTemperature).(string)
	humi := tc.GetOutput(ovHumidity).(string)

	assert.NotNil(t, temp)
	assert.NotNil(t, humi)

	fmt.Printf("Temperature: %f - Humidity: %f\n", temp, humi)

}
