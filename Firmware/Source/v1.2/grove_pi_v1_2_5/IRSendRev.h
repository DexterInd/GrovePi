/*
 * IRremote
 * Version 0.11 August, 2009
 * Copyright 2009 Ken Shirriff
 * For details, see http://arcfn.com/2009/08/multi-protocol-infrared-remote-library.html
 * 
 * Modified by Paul Stoffregen <paul@pjrc.com> to support other boards and timers
 * Modified  by Mitra Ardron <mitra@mitra.biz> 
 * Added Sanyo and Mitsubishi controllers
 * Modified Sony to spot the repeat codes that some Sony's send
 * 
 * Modifier by
 * Interrupt code based on NECIRrcv by Joe Knapp
 * http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1210243556
 * Also influenced by http://zovirl.com/2008/11/12/building-a-universal-remote-with-an-arduino/
 * 
 * Modified by 
 * http://www.seeedstudio.com/ 
 * For the Grove-IR receiver and Grove-Infrared Emitter
 * JVC and Panasonic protocol added by Kristian Lauszus (Thanks to zenwheel and other people at the original blog post)
 */

#ifndef _IRSENDREV_H_
#define _IRSENDREV_H_

// len, start_H, start_L, nshort, nlong, data_len, data[data_len]....
#define D_LEN       0
#define D_STARTH    1
#define D_STARTL    2
#define D_SHORT     3
#define D_LONG      4
#define D_DATALEN   5
#define D_DATA      6


#define USECPERTICK 50  // microseconds per clock interrupt tick
#define RAWBUF 300 // Length of raw duration buffer

// Marks tend to be 100us too long, and spaces 100us too short
// when received due to sensor lag.
#define MARK_EXCESS 100

#define __DEBUG     0

// Results returned from the decoder
class decode_results {

    public:
    volatile unsigned int *rawbuf; // Raw intervals in .5 us ticks
    int rawlen;           // Number of records in rawbuf.
};

// main class for receiving IR
class IRSendRev
{
    private:
    decode_results results;
    //**************************rev**********************************
    
    private:
    int decode(decode_results *results);
    void enableIRIn();
    
    public:

    void Init(int revPin);                          // init
    void Init();
    unsigned char Recv(unsigned char *revData);     // 
    unsigned char IsDta();                          // if IR get data
    void Clear();                                   // clear IR data

    //**************************send*********************************
    private:

    void sendRaw(unsigned int buf[], int len, int hz);

    // private:
    
    void mark(int usec);
    void space(int usec);
	void enableIROut(int khz);
    
    public:
    
    void Send(unsigned char *idata, unsigned char ifreq);

};

extern IRSendRev IR;

#endif
