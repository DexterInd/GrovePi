package main

import (
	"github.com/JGrotex/GrovePi/Software/Go/grovepi"

	"fmt"
)

func runDHT() string {
	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	defer g.CloseDevice()

	t, h, err := g.ReadDHT(grovepi.D4)

	if err != nil {
		panic(err)
	}

	fmt.Printf("Temperature: %f - Humidity: %f\n", t, h)

	return "done"
}
