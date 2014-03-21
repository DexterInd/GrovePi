package main

import (
	"./grovepi"
	"fmt"
	"time"
)

func main() {
	var g grovepi.GrovePi
	g = *grovepi.InitGrovePi(0x04)
	for {
		time.Sleep(2 * time.Second)
		t, h, err := g.ReadDHT(grovepi.D4)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(t)
		fmt.Println(h)
	}
	g.CloseDevice()
}
