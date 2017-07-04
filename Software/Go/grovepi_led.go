package main

import (
	"./grovepi"
	"fmt"
	"time"
)

func main() {
	g := *grovepi.NewGrovePi(0x04)
	
	for {
		g.DigitalWrite(grovepi.D2, 1)
		time.Sleep(500 * time.Millisecond)
		g.DigitalWrite(grovepi.D2, 0)
		time.Sleep(500 * time.Millisecond)
	}
}
