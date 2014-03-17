package main

import (
	"./grovepi"
	"fmt"
	"time"
)

func main() {
	var d grovepi.GrovePi
	d = *grovepi.InitGrovePi(0x04)
	for {
		time.Sleep(2 * time.Second)
		t, h, err := d.ReadDTH(grovepi.D4)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(t)
		fmt.Println(h)
	}
	d.CloseDevice()
}
