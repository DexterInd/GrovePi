package main

import (
	"./grovepi"

	"fmt"
)

func main() {

	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	defer g.CloseDevice()

	for {
		t, h, err := g.ReadDHT(grovepi.D4)

		if err != nil {
			panic(err)
		}

		fmt.Printf("Temperature: %f - Humidity: %f\n", t, h)
	}

}
