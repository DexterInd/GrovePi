package main

import (
	"fmt"
	"time"

	"github.com/JGrotex/GrovePi/Software/Go/grovepi"
)

func runLED() string {
	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	err := g.PinMode(grovepi.D3, "output")
	if err != nil {
		fmt.Println(err)
	}

	g.DigitalWrite(grovepi.D3, 1)
	time.Sleep(500 * time.Millisecond)
	g.DigitalWrite(grovepi.D3, 0)
	time.Sleep(500 * time.Millisecond)

	return "done"
}

func main() {
	runLED()
}
