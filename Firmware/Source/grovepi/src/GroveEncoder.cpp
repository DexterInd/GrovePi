/**
 * GroveEncoder.cpp - Grove Encoder library
 *
 * Copyright (C) 2016 David Antler
 * All rights reserved.
 *
 * This software may be modified and distributed under the terms
 * of the included license.  See the LICENSE file for details.
 */

#include "GroveEncoder.h"
#include "Arduino.h"

/*****************   HELPER FUNCTIONS  ********************/

#define GROVE_ENC_LOGGING     0

#if GROVE_ENC_LOGGING
 #define DUMP_STATE() { \
       Serial.println("* * * DUMP * * *"); \
       Serial.print(" pinA  :  "); Serial.print(pinA); Serial.println(""); \
       Serial.print(" pinB  :  "); Serial.print(pinB); Serial.println(""); \
       Serial.print(" stage :  "); Serial.print(stage - STAGE_ZERO, HEX);  Serial.println(""); \
       Serial.print(" rot   :  "); Serial.print(rotation); Serial.println(""); \
 }
#else
 #define DUMP_STATE()  {}
#endif

// Unfortunately we need to use a singleton
GroveEncoder* singleton;

// State machine for parsing encoded data
enum Stage {
  STAGE_UNDEF = 0x0f,
  STAGE_ZERO  = 0x10,
  STAGE_ONE   = 0x11,
  STAGE_TWO   = 0x12,
  STAGE_THREE = 0x13,
  STAGE_FOUR  = 0x14
};

// Another piece of state for rotation state machine
enum Rotation {
  CLOCKWISE = 2,
  COUNTERCLOCKWISE = 3,
  UNCERTAIN = 4
};

#define INDEX_MASK(indexValue) (indexValue & (PIN_DATA_SIZE - 1))

inline bool GroveEncoder::pushToQueue(unsigned char myValue)
{
  if(queueIsFull()) {
    Serial.println("Queue full, overwriting!");
  }
  pinDataQueue[INDEX_MASK(writeIndex)] = myValue;
  writeIndex++;
  return true;
}

inline bool GroveEncoder::queueIsEmpty()
{
  return writeIndex == readIndex;
}

inline bool GroveEncoder::queueIsFull()
{
  return (writeIndex - readIndex) >= PIN_DATA_SIZE;
}

inline unsigned char GroveEncoder::popFromQueue()
{
  unsigned char outValue = 0xFF;
  if(!queueIsEmpty()) {
    outValue = pinDataQueue[INDEX_MASK(readIndex)];
    readIndex++;
  } else {
    Serial.println("Popped from empty queue");
  }
  return outValue;
}

// This function only exists due to the singleton issue.
void GroveEncoder::privateIntHandler()
{
  singleton->updateEncoderFast();
}

// This routine is supposed to be very very fast.
void GroveEncoder::updateEncoderFast()
{
  unsigned char newValue;
  newValue = (unsigned char)(digitalRead(LOW_PIN) + (digitalRead(HIGH_PIN) << 1));
  // Push to Queue
  pushToQueue(newValue);

  // Do deferrable "slow" work when steady (e.g. both pins are high)
  if(newValue == 3) {
    processQueue();

    if(optCallBack != NULL) {
      // Only process the callback if there's new data to post.
      static int prevValue = 0xDEADBEEF; // squelch the warning.
      if (value != prevValue) {
        prevValue = value;
        optCallBack(value);
      }
    }
  }
}

#define GET_A_NEW_BYTE() { \
    if(queueIsEmpty()) return;            \
    unsigned char pins = popFromQueue();  \
    pinA = pins & 0x01;                   \
    pinB = (pins & 0x02) >> 1;            \
}

/**
 * Processes the queue of bytes
 */
void GroveEncoder::processQueue()
{
  int pinA, pinB;
  char stage = STAGE_ZERO;
  Rotation rotation = UNCERTAIN;

  GET_A_NEW_BYTE();

  do {

    DUMP_STATE();
    if ((pinA == pinB) && (pinB == HIGH)) {
      GET_A_NEW_BYTE();
      stage = STAGE_ZERO;
      rotation = UNCERTAIN;
      continue;
    }

    switch(stage) {

      case STAGE_ZERO:
        // Stage zero means that we might be at the "rising" edge of our rotation.
        // Decide if CW, CCW, or throw-away.
        if (pinA > pinB) {
          // clockwise
          rotation = CLOCKWISE;
          stage = STAGE_ONE;
        } else if (pinA < pinB) {
          // ccw
          rotation = COUNTERCLOCKWISE;
          stage = STAGE_ONE;
        }
        GET_A_NEW_BYTE();
        break;

      case STAGE_ONE:
        // In stage one, we've identified our direction, but have not yet seen double-zeros.
        // Once we see double zeros, lets fall through to stage two.
        if ((LOW == pinB) && (pinA == LOW)) {
          stage = STAGE_TWO;
          continue;
        }

        stage = STAGE_ZERO;
        break;

      case STAGE_TWO:
        // Stage two means we have seen double zeros, but can escape by getting anything else.
        if ((pinB == LOW) && (pinA == LOW)) {
          GET_A_NEW_BYTE();
          continue;
        } else if (pinA ^ pinB) {
          stage = STAGE_THREE;
          continue;
        } else {
          stage = STAGE_ZERO;
          continue;
        }

      case STAGE_THREE:
        // Stage three means that we are at the "falling" edge of our rotation.
        // Lets check to make sure we are being consistent.
        if (rotation == CLOCKWISE) {
          if(pinA < pinB ) {
            stage = STAGE_FOUR;
          } else {
            // failed to stay consistent!
            stage = STAGE_ZERO;
          }
        }
        else if (rotation == COUNTERCLOCKWISE) {
          if(pinA > pinB) {
            stage = STAGE_FOUR;
          } else {
            // failed to stay consistent!
            stage = STAGE_ZERO;
          }
        }
        continue;

      case STAGE_FOUR:
        // Stage four is logging the results!
        if (rotation == CLOCKWISE) {
          value++;
        } else if (rotation == COUNTERCLOCKWISE) {
          value--;
        }
        stage = STAGE_ZERO;
        GET_A_NEW_BYTE();
        continue;

      default:
        Serial.println("Default is bad");
        DUMP_STATE();
        break;
    }
  } while(!queueIsEmpty());
}

/*****************    API FUNCTIONS    ********************/

// Gets the value on the encoder.  It's an integer, positive or negative.
int GroveEncoder::getValue()
{
    return value;
}

void GroveEncoder::resetValue()
{
    setValue(0);
}

void GroveEncoder::setValue(int newValue)
{
    value = newValue;
}

/**
 * This will enumerate a GroveEncoder on a particular pin.
 * You can provide an optional callback, or poll the "getValue()" API.
 */
GroveEncoder::GroveEncoder(int pin, void (*optionalCallBack)(int))
{
  // Needed to make GroveEncoder a singleton because attachInterrupt doesn't take a parameter!
  singleton = this;
#if GROVE_ENC_LOGGING
  Serial.begin(9600);
  Serial.print("Starting Grove Encoder debug logging...");
#endif

  // Initialize values
  writeIndex = readIndex = 0;
  LOW_PIN = pin;
  HIGH_PIN = pin + 1;
  value = 0;
  optCallBack = optionalCallBack;

  // Initialize pins
  pinMode(LOW_PIN, INPUT_PULLUP);
  pinMode(HIGH_PIN, INPUT_PULLUP);

#if GROVE_ENC_LOGGING
  // Expect these to be low right now.
  if(digitalRead(LOW_PIN) || digitalRead(HIGH_PIN)) {
    // Unless you're actively playing with the encoder, these will be low...
    Serial.print("Grove Encoder library thinks you have a wiring issue!");
  }
#endif

  // Set up interrupts
  attachInterrupt(digitalPinToInterrupt(LOW_PIN),  privateIntHandler, CHANGE);
  attachInterrupt(digitalPinToInterrupt(HIGH_PIN), privateIntHandler, CHANGE);
}

