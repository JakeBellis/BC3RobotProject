#include <Printers.h>
#include <XBee.h>

XBee xbee = XBee();

Rx16Response rx16 = Rx16Response();
Rx64Response rx64 = Rx64Response();

uint8_t option = 0;
uint8_t data[30] = {};

unsigned long start = millis();
bool startFlag = 0; //false before transmit is ready


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //serial usb to computer
  Serial1.begin(9600); //serial for xbee communication
  Serial.println("serial start");
  xbee.setSerial(Serial1);
}

void loop() {
  // put your main code here, to run repeatedly:
	xbeeReceive();

}

void xbeeReceive(){
  xbee.readPacket();
  if (xbee.getResponse().isAvailable()) {
	  // got something
	  Serial.println("received communication");
	  //for (int i = 0; sizeof(data); i++) {
		//  data[i] = 0;
	  //}

	  if (xbee.getResponse().getApiId() == RX_16_RESPONSE || xbee.getResponse().getApiId() == RX_64_RESPONSE) {
		  // got a rx packet

		  if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
			  Serial.println("16 bit response received");
			  xbee.getResponse().getRx16Response(rx16);
			  option = rx16.getOption();
			  for (int i = 0; i < rx16.getDataLength(); i++) {
				  data[i] = rx16.getData(i);
				  Serial.print(F("0x")); Serial.print(data[i],HEX); Serial.print(" "); //print packet hex data
			  }
		      Serial.println();
		  }
		  else {
			  xbee.getResponse().getRx64Response(rx64);
			  option = rx64.getOption();
			  for (int i = 0; i < rx64.getDataLength(); i++) {
				  data[i] = rx64.getData(i);
			  }
		  }

		  for (int i = 0; i < sizeof(data); i++) {
			  Serial.print(data[i] + " ");
		  }
		  Serial.println();


	  }
	  else if (xbee.getResponse().isError()) {
		  //nss.print("Error reading packet.  Error code: ");  
		  //nss.println(xbee.getResponse().getErrorCode());
		  // or flash error led
	  }
  }
}
