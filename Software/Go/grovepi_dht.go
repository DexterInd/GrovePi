package main

import (
	"fmt"
	// To be replaced with a proper repo path
	"./grove"
)

func main() {
	g := *grovepi.NewGrovePi(0x04)
	defer g.Close()

	for {
		t, h, err := g.ReadDHT(grovepi.D4)

		if err != nil {
			panic(err)
		}

		fmt.Printf("Temperature: %f - Humidity: %f\n", t, h)
	}

}
