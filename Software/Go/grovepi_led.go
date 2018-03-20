package main

import (
	"./grovepi"
	"fmt"
	"time"
)

func main() {
	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	err := g.PinMode(grovepi.D3, "output")
	if err != nil {
		fmt.Println(err)
	}

	for {
		g.DigitalWrite(grovepi.D3, 1)
		time.Sleep(500 * time.Millisecond)
		g.DigitalWrite(grovepi.D3, 0)
		time.Sleep(500 * time.Millisecond)
	}
}
