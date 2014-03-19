package main

import (
	"./grovepi"
	"fmt"
	"time"
)

func main() {
	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	err := g.PinMode(grovepi.D2, "output")
	if err != nil {
		fmt.Println(err)
	}
	for {
		g.DigitalWrite(grovepi.D2, 1)
		time.Sleep(500 * time.Millisecond)
		g.DigitalWrite(grovepi.D2, 0)
		time.Sleep(500 * time.Millisecond)
	}
}
