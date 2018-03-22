package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestLED(t *testing.T) {
	fmt.Println("start test now ...")
	var result = runLED()
	assert.Equal(t, "done", result, "should return 'done'")
}

func TestDHT(t *testing.T) {
	fmt.Println("start test now ...")
	var result = runDHT()
	assert.Equal(t, "done", result, "should return 'done'")
}
