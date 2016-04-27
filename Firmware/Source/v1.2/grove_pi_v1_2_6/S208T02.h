#ifndef S208T02_H
#define S208T02_H
#if ARDUINO >= 100
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif

/* S208T02 library 

MIT license
written by Pernecker Sébastien
*/

class S208T02 {
  private: 
    uint8_t _pin,_percent;
    float _highTimeMs,_lowTimeMs,_error,_error_high,_error_low;    
    boolean _fanStarted,_pinSet;
    uint8_t _cpt;
    int add_error;
  public:
    void begin();  
    void setFanControllerState(boolean state);
    void setPin(uint8_t pin);  
    void controlFanSpeed(uint8_t percent);
    void checkFanStatus();    
};
#endif