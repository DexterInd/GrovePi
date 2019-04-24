/**
 * GroveEncoder.h - Header for Grove Encoder library
 *
 * Copyright (C) 2016 David Antler
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the included license.  See the LICENSE file for details.
 */

#ifndef GROVE_ENCODER_LIB_H_
#define GROVE_ENCODER_LIB_H_

// Note: PIN_DATA_SIZE must be a power of two due to the queue implementation.
#define PIN_DATA_SIZE 128

class GroveEncoder {

  public:
    GroveEncoder(int pin, void (*optionalCallBack)(int));
    int getValue();
    void setValue(int newValue);
    void resetValue();

    // This is private, but it needs to be public/static
    static void privateIntHandler();
    void updateEncoderFast();

  private:
    int LOW_PIN, HIGH_PIN;
    volatile int value;
    int readIndex;
    int writeIndex;
    unsigned char pinDataQueue[PIN_DATA_SIZE];
    void (*optCallBack)(int);

    inline bool pushToQueue(unsigned char myValue);
    inline bool queueIsEmpty();
    inline bool queueIsFull();
    inline unsigned char popFromQueue();
    void processQueue();
};

#endif

