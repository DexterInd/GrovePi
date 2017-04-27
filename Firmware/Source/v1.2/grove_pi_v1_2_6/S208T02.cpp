/* DHT library 

MIT license
written by Pernecker Sébastien
*/

#include "S208T02.h"
#include <math.h>

void S208T02::begin() {
  _cpt=0;
  _fanStarted=0;
  _pinSet=0;
  _highTimeMs = 0;
  _lowTimeMs = 255;
  _error=0;
  _error_low=0;
  _error_high=0;
}
    
void S208T02::setPin(uint8_t pin) {
  // set up the pins!
  _pin = pin;
  pinMode(_pin, OUTPUT);
  digitalWrite(_pin, LOW);
  _pinSet=1;
}
    
void S208T02::checkFanStatus(void)
{
  if(_fanStarted)
  {
     if(_percent==0)
     {
       digitalWrite(_pin, LOW);
     }else if (_percent<50){
       if(_cpt<_highTimeMs)
       {
         digitalWrite(_pin, HIGH);                  
         _cpt++;
       }else{
         digitalWrite(_pin, LOW);         
         if(round(_error)>1)
         {
           add_error+=1;
           if(_error>1)
           {
             _error-=1;
           }
         }
         if(_cpt>=(round(_lowTimeMs)+add_error))
         {           
           add_error=0;                      
           _cpt=0;
         }else{
           _cpt++;
         }
         _error+=_error_low;                      
       }
     }else if (_percent==50){
       if((_cpt++%2)==0){
         digitalWrite(_pin, LOW);
       }else{
         digitalWrite(_pin, HIGH);
       }
     }else if (_percent<100) {
       if(_cpt<_lowTimeMs)
       {
         digitalWrite(_pin, LOW);
         if(_error>1)
         {
           _error-=1;
         }
         _cpt++;
       }else{
         digitalWrite(_pin, HIGH);         
         if(round(_error)>1)
         {
           add_error+=1;
           if(_error>1)
           {
             _error-=1;
           }
         }
         if(_cpt>=(round(_highTimeMs)+add_error))
         {           
           add_error=0;                      
           _cpt=0;
         }else{
           _cpt++;
         }       
         _error+=_error_high;
       }
     }else if (_percent>=100){
       digitalWrite(_pin, HIGH);                 
     }  
   }
}

    
void S208T02::setFanControllerState(boolean state)
{
  if(_pinSet)
  {
    _fanStarted=state;
  }
}

void S208T02::controlFanSpeed(uint8_t percent)
{
  _percent=percent;
  if(_percent==0)
  {
    _highTimeMs=0;
    _lowTimeMs=255;
  }else if(_percent<=50){
    _highTimeMs=1;
    _lowTimeMs=((float)(100-_percent))/((float)_percent);
    _error_low=_lowTimeMs-round(_lowTimeMs);
  }else if(_percent<100){
    _lowTimeMs=1;
    _highTimeMs=((float)_percent)/((float)(100-_percent));
    _error_high=_highTimeMs-round(_highTimeMs);
  }else{
    _lowTimeMs=0;
    _highTimeMs=255;    
  }
  _cpt=0;
  _error=0;
}

