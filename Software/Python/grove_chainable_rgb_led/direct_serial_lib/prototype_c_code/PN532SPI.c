/*
The original files can be found in http://blog.iteadstudio.com/to-drive-itead-pn532-nfc-module-with-raspberry-pi/
All the contents are based on that article. I made some modification to the file, removed P2P communication, simplified some codes.

This files(include the header file and source file) are modified by @DaochenShi (shidaochen@live.com)
*/

#include "PN532SPI.h"

//#define PN532DEBUG

byte pn532ack[] = {0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00};
byte pn532response_firmwarevers[] = {0x00, 0xFF, 0x06, 0xFA, 0xD5, 0x03};

#define PN532_PACK_BUFF_SIZE 64
#define SPISPEED 1000000

byte pn532_packetbuffer[PN532_PACK_BUFF_SIZE];

/*Construct PN532 object and construct PN532's own SPI interface object */
int i,j;
unsigned char a=0xaa;
void initialPN532SPI()
{
	j = wiringPiSetup();
	wiringPiSPISetup(channel, SPISPEED);
#ifdef PN532DEBUG
	printf("wiringPiSetup is %d\n",j);
#endif

#ifdef CHIPSELECT
	pinMode(_chipSelect, OUTPUT);

	digitalWrite(_chipSelect, HIGH);
	digitalWrite(_chipSelect, LOW);
#endif

	sleep(1);

	pn532_packetbuffer[0] = PN532_FIRMWAREVERSION;

	sendCommandCheckAck(pn532_packetbuffer, 1, 1000);
#ifdef CHIPSELECT
	//digitalWrite(_chipSelect, HIGH);	// to prevent wrong select.
#endif
}


uint32_t getFirmwareVersion(void)
{
	uint32_t response;

	pn532_packetbuffer[0] = PN532_FIRMWAREVERSION;

	if (!sendCommandCheckAck(pn532_packetbuffer, 1, 1000))
	return 0;

	//nfcPN532Read data packet
	nfcPN532Read(pn532_packetbuffer, 12);
	//Check response headers.
	if (0 != strncmp((char *)pn532_packetbuffer, (char *)pn532response_firmwarevers, 6)) 
	{
#ifdef PN532DEBUG
	for (response = 0; response < 12; response++)
	{
		printf("%X ", pn532response_firmwarevers[response]);
	}
	printf("\n");
#endif
		return 0;
	}

	response = pn532_packetbuffer[6];
	response <<= 8;
	response |= pn532_packetbuffer[7];
	response <<= 8;
	response |= pn532_packetbuffer[8];
	response <<= 8;
	response |= pn532_packetbuffer[9];

	return response;
}

/**********************************************************************/
/*Function: Send command to PN532 with SPI and check the ACK.          */
/*Parameter:-uint8_t* cmd,The pointer that saves the command code to be sent;*/
/*          -uint8_t cmd_len,The number of bytes of the command;        */
/*	    -uint16_t timeout,default timeout is one second            */
/*Return:   boolean,ture = send command successfully	               */
boolean sendCommandCheckAck(uint8_t* cmd, uint8_t cmd_len, uint16_t timeout) 
{
	uint16_t timer = 0;

	// nfcPN532Write the command
	writeCommand(cmd, cmd_len);

	// Wait for chip to say it's ready!
	while (readSpiStatus() != PN532_SPI_READY)
	{
		if (timeout != 0)
		{
			timer+=20;
			if (timer > timeout)
			{
#ifdef PN532DEBUG
			printf("timeout\n");
#endif
			return false;
			}
		}
		usleep(20 * 1000);
	}

	// nfcPN532Read acknowledgement
	if (!checkSpiAck())
	{
#ifdef PN532DEBUG
		printf("spi no answer\n");
#endif
		return false;
	}

	timer = 0;
#ifdef PN532DEBUG
	printf("check spi finsh\n");
#endif
	// Wait for chip to say its ready!
	while (readSpiStatus() != PN532_SPI_READY)
	{
		if (timeout != 0)
		{
			timer+=20;
			if (timer > timeout)
#ifdef PN532DEBUG
			printf("nfcPN532Read spi timeout\n");
#endif
			return false;
		}
		usleep(20 * 1000);
	}
#ifdef PN532DEBUG
	printf("the spi return ture\n");
#endif
	return true; // ack'd command
}

boolean SAMConfig(void) 
{
	pn532_packetbuffer[0] = PN532_SAMCONFIGURATION;
	pn532_packetbuffer[1] = 0x01; // normal mode;
	pn532_packetbuffer[2] = 0x14; // timeout 50ms * 20 = 1 second
	pn532_packetbuffer[3] = 0x01; // use IRQ pin! What's that?

	if (! sendCommandCheckAck(pn532_packetbuffer, 4,1000))
	return false;

	// nfcPN532Read data packet
	nfcPN532Read(pn532_packetbuffer, 8);

	return  (pn532_packetbuffer[5] == 0x15);
}


uint32_t authenticateBlock(uint8_t cardnumber /*1 or 2*/,uint32_t cid /*Card NUID*/, uint8_t blockaddress /*0 to 63*/,uint8_t authtype/*Either KEY_A or KEY_B */, uint8_t * keys) 
{

	pn532_packetbuffer[0] = PN532_INDATAEXCHANGE;
	pn532_packetbuffer[1] = cardnumber;  	// either card 1 or 2 (tested for card 1)

	if(authtype == KEY_A)
	{
		pn532_packetbuffer[2] = PN532_AUTH_WITH_KEYA;
	}
	else
	{
		pn532_packetbuffer[2] = PN532_AUTH_WITH_KEYB;
	}
	pn532_packetbuffer[3] = blockaddress; //This address can be 0-63 for MIFARE 1K card

	pn532_packetbuffer[4] = keys[0];
	pn532_packetbuffer[5] = keys[1];
	pn532_packetbuffer[6] = keys[2];
	pn532_packetbuffer[7] = keys[3];
	pn532_packetbuffer[8] = keys[4];
	pn532_packetbuffer[9] = keys[5];

	pn532_packetbuffer[10] = ((cid >> 24) & 0xFF);
	pn532_packetbuffer[11] = ((cid >> 16) & 0xFF);
	pn532_packetbuffer[12] = ((cid >> 8) & 0xFF);
	pn532_packetbuffer[13] = ((cid >> 0) & 0xFF);

	if (! sendCommandCheckAck(pn532_packetbuffer, 14,1000))
	return false;

	// nfcPN532Read data packet
	nfcPN532Read(pn532_packetbuffer, 2+6);

#ifdef PN532DEBUG
	int iter = 0;
	for(iter=0;iter<14;iter++)
	{
		printf("%X ",(pn532_packetbuffer[iter]));
	}
	printf("\n");
	// check some basic stuff

	printf("AUTH");
	for(i=0;i<2+6;i++)
	{
		printf("%d\n",(pn532_packetbuffer[i]));
		printf(" ");
	}
#endif

	if((pn532_packetbuffer[6] == 0x41) && (pn532_packetbuffer[7] == 0x00))
	{
		return true;
	}
	else
	{
		return false;
	}

}
/****************************************************************************/
/*Function: nfcPN532Read a block(16 bytes) from the tag and stores in the parameter.*/
/*Parameter:-uint8_t cardnumber,can be 1 or 2;                              */
/*          -blockaddress,range from 0 to 63;                               */
/*	    -uint8_t* block,will save 16bytes that nfcPN532Read from tag.           */
/*Return:   boolean         					      	    */
boolean readMemoryBlock(uint8_t cardnumber,uint8_t blockaddress,uint8_t * block)
{
	uint8_t i;

	pn532_packetbuffer[0] = PN532_INDATAEXCHANGE;
	pn532_packetbuffer[1] = cardnumber;  // either card 1 or 2 (tested for card 1)
	pn532_packetbuffer[2] = PN532_MIFARE_READ;
	pn532_packetbuffer[3] = blockaddress; //This address can be 0-63 for MIFARE 1K card

	if (! sendCommandCheckAck(pn532_packetbuffer, 4,1000))
	return false;

	nfcPN532Read(pn532_packetbuffer, 64);
#ifdef PN532DEBUG
	for( i = 0; i < 64; i++)
	{
		printf("%x ", pn532_packetbuffer[i]);
		if(i%8==7)
			printf("\r\n");
	}
#endif
	
	// nfcPN532Read data packet
	nfcPN532Read(pn532_packetbuffer, 18+6);
	// check some basic stuff
#ifdef PN532DEBUG
	printf("nfcPN532Read");
#endif
	for(i=8;i<18+6;i++)
	{
		block[i-8] = pn532_packetbuffer[i];
#ifdef PN532DEBUG
		printf("%d\n",(pn532_packetbuffer[i])); 
#endif
	}

	if((pn532_packetbuffer[6] == 0x41) && (pn532_packetbuffer[7] == 0x00))
	{
		return true; 		//nfcPN532Read successful
	}
	else
	{
		return false;
	}

}

/****************************************************************************/
/*Function: nfcPN532Write a block(16 bytes) to the tag.                             */
/*Parameter:-uint8_t cardnumber,can be 1 or 2;                              */
/*          -blockaddress,range from 0 to 63;                               */
/*	    -uint8_t* block,saves 16bytes that will nfcPN532Write to the tag.       */
/*Return:  boolean							    */
/*Note:Donot nfcPN532Write to Sector Trailer Block unless you know what you are doing.*/
boolean writeMemoryBlock(uint8_t cardnumber,uint8_t blockaddress,uint8_t * block) 
{
	uint8_t bytes;

	pn532_packetbuffer[0] = PN532_INDATAEXCHANGE;
	pn532_packetbuffer[1] = cardnumber;  		// either card 1 or 2 (tested for card 1)
	pn532_packetbuffer[2] = PN532_MIFARE_WRITE;
	pn532_packetbuffer[3] = blockaddress;

	for(bytes = 0; bytes < 16; bytes++)
	{
		pn532_packetbuffer[4+bytes] = block[bytes];
	}

	if (! sendCommandCheckAck(pn532_packetbuffer, 20,1000))
	return false;
	// nfcPN532Read data packet
	nfcPN532Read(pn532_packetbuffer, 2+6);

#ifdef PN532DEBUG
	// check some basic stuff
	printf("nfcPN532Write");

	for(i=0;i<2+6;i++)
	{
		printf("%d\n",(pn532_packetbuffer[i])); 

	}
	printf("\n");
#endif

	if((pn532_packetbuffer[6] == 0x41) && (pn532_packetbuffer[7] == 0x00))
	{
		return true; 									//nfcPN532Write successful
	}
	else
	{
		return false;
	}
}

uint32_t readPassiveTargetID(uint8_t cardbaudrate) 
{
	uint32_t cid;
	uint16_t sens_res;
	uint8_t i;

	pn532_packetbuffer[0] = PN532_INLISTPASSIVETARGET;
	pn532_packetbuffer[1] = 1;  	// max 1 cards at once (we can set this to 2 later)
	pn532_packetbuffer[2] = cardbaudrate;

	if (! sendCommandCheckAck(pn532_packetbuffer, 3,1000))
	return 0x0;  					// no cards nfcPN532Read

	// nfcPN532Read data packet 
	nfcPN532Read(pn532_packetbuffer, 20);// why 20?! buffer total is 64!
	// check some basic stuff

#ifdef PN532DEBUG
	printf("Found ");
	printf("%d",(pn532_packetbuffer[7]));
	printf(" tags\n");
#endif

	if (pn532_packetbuffer[7] != 1)
	return 0;

	sens_res = pn532_packetbuffer[9];
	sens_res <<= 8;
	sens_res |= pn532_packetbuffer[10];
#ifdef PN532DEBUG
	printf("Sens Response: ");
	printf("%d\n",(sens_res));
	printf("Sel Response: ");
	printf("%d",(pn532_packetbuffer[11]));
	printf("\n");
#endif
	cid = 0;

	for (i=0; i< pn532_packetbuffer[12]; i++)
	{
		cid <<= 8;
		cid |= pn532_packetbuffer[13+i];
#ifdef PN532DEBUG
		printf(" 0x");
		printf("%X\n",(pn532_packetbuffer[13+i]));
#endif
	}

#ifdef PN532DEBUG
	printf("TargetID");
	for(i=0;i<20;i++)
	{
		printf("%d\n",(pn532_packetbuffer[i])); 
	}
	printf("\n");
#endif
	return cid;
}

/**********************************************************************/
/*Function: nfcPN532Read n bytes data and it stores in the parameter .        	*/
/*Parameter:-uint8_t* buff,saves the data nfcPN532Read from PN532;            	*/
/*	    -uint8_t n,tells it wll nfcPN532Read n bytes.                     		*/
/*Return:  void                                                       	*/
void nfcPN532Read(uint8_t* buff, uint8_t n) 
{
	uint8_t i;
#ifdef CHIPSELECT
	digitalWrite(_chipSelect, LOW);
#endif
	usleep(2000);
	nfcPN532Write(PN532_SPI_DATAREAD);

#ifdef PN532DEBUG
	printf("Reading:\n");
#endif

	for (i=0; i < n; i ++) 
	{
		usleep(1000);
		buff[i] = readF();
#ifdef PN532DEBUG
		printf("debug readf is %d\n",buff[i]);
#endif
	}
#ifdef CHIPSELECT
	digitalWrite(_chipSelect, HIGH);
#endif
}

void writeCommand(uint8_t* cmd, uint8_t cmd_len)
{
	uint8_t checksum;
	uint8_t cmdlen_1;
	uint8_t i;
	uint8_t checksum_1;

	cmd_len++;

#ifdef PN532DEBUG
	printf("Sending: \n");
#endif

#ifdef CHIPSELECT
	digitalWrite(_chipSelect, LOW);
#endif	
	usleep(2000);	// or whatever the delay is for waking up the board

	nfcPN532Write(PN532_SPI_DATAWRITE);	//0x01

	checksum = PN532_PREAMBLE + PN532_PREAMBLE + PN532_STARTCODE2;
	nfcPN532Write(PN532_PREAMBLE);		//0x00
	nfcPN532Write(PN532_PREAMBLE);		//0x00
	nfcPN532Write(PN532_STARTCODE2);	//0xff

	nfcPN532Write(cmd_len);			//0x02
	cmdlen_1 = ~cmd_len + 1;
	nfcPN532Write(cmdlen_1);		//0x01

	nfcPN532Write(PN532_HOSTTOPN532);	//0xd4
	checksum += PN532_HOSTTOPN532;

#ifdef PN532DEBUG
	printf("preamble is %X\n",(PN532_PREAMBLE));
	printf("startcode2 is %X\n",(PN532_STARTCODE2));
	printf("cmd_len is %X\n",(cmd_len));
	printf("cmdlen_1 is %X\n",(cmdlen_1));
	printf("hosttopn532 is %X\n",(PN532_HOSTTOPN532));
#endif

	for (i=0; i<cmd_len-1; i++) 
	{
		nfcPN532Write(cmd[i]);
		checksum += cmd[i];
#ifdef PN532DEBUG
		printf("cmd[i] is %X\n",(cmd[i]));
#endif
	}

	checksum_1 = ~checksum;
	nfcPN532Write(checksum_1);
	nfcPN532Write(PN532_POSTAMBLE);
#ifdef CHIPSELECT
	digitalWrite(_chipSelect, HIGH);
#endif	

#ifdef PN532DEBUG
	printf("checksum is %d\n", (checksum_1));
	printf("postamble is %d\n", (PN532_POSTAMBLE));
	printf("postamble is %d\n", (PN532_POSTAMBLE));
#endif
}
/************** high level SPI */
boolean checkSpiAck()
{
	uint8_t ackbuff[6];
	nfcPN532Read(ackbuff, 6);
	return (0 == strncmp((char *)ackbuff, (char *)pn532ack, 6));
}

/************** mid level SPI */
uint8_t readSpiStatus(void) 
{
	uint8_t status;

#ifdef CHIPSELECT
	digitalWrite(_chipSelect, LOW);
#endif
	usleep(2000);
	nfcPN532Write(PN532_SPI_STATREAD);
	status = readF();
#ifdef CHIPSELECT
	digitalWrite(_chipSelect, HIGH);
#endif
	return status;
}

/************** low level SPI ********/
/*Function:Transmit a byte to PN532 through the SPI interface. */
void nfcPN532Write(uint8_t _data)
{
	unsigned char writeData = 0, p;

	for(p=0;p<8;p++)
	{
		if(_data & 0x01)
			writeData |= 1<<(7-p);

		_data = _data>>1;
	}
	wiringPiSPIDataRW(channel, &writeData, 1);

}

/*Function:Receive a byte from PN532 through the SPI interface */
uint8_t readF(void)
{
	unsigned char readData,redata = 0,p;
	wiringPiSPIDataRW(channel, &readData, 1);

	for(p=0;p<8;p++)
	{
		if(readData & 0x01)
		{
			redata |= 1<<(7-p);
		}
		readData = readData >> 1;
	}
	return redata;
}


