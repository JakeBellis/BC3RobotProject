#include <Printers.h>
#include <XBee.h>

XBee xbee = XBee();

Rx16Response rx16 = Rx16Response();
Rx64Response rx64 = Rx64Response();
const int BASE_ADDRESS = 0x0036;

bool newCommandFlag = 0;


// 16-bit addressing: Enter address of remote XBee, typically the coordinator
uint8_t ack[] = { 0, 0, 0 }; //ack is {command, distance, completed} echoes command and says if completed
uint8_t coords[] = {0,0,0,0};

Tx16Request txAck = Tx16Request(BASE_ADDRESS, ack, sizeof(ack)); 
Tx16Request txCoords = Tx16Request(BASE_ADDRESS, coords, sizeof(coords));
TxStatusResponse txStatus = TxStatusResponse();

uint8_t option = 0;
struct commands{
	uint8_t data[30];
};

unsigned long start = millis();
bool startFlag = 0; //false before transmit is ready

commands xbeeReceive();
void xbeeAck();
//void xbeeSendCoords();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); //serial usb to computer
  Serial1.begin(9600); //serial for xbee communication
  Serial.println("serial start");
  Serial.println(sizeof(ack));
  xbee.setSerial(Serial1);
}

void loop() {
  // put your main code here, to run repeatedly:
	commands commandArray = commands();
	commandArray = xbeeReceive();
	ack[0] = commandArray.data[0];
	ack[1] = commandArray.data[1];
	ack[2] = 1;
	xbeeAck();
	
}

commands xbeeReceive(){
	commands cmd = commands();
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
			  int i = 0;
			  for (i = 0; i < rx16.getDataLength(); i++) {
				  cmd.data[i] = rx16.getData(i);
				  Serial.print(F("0x")); Serial.print(cmd.data[i],HEX); Serial.print(" "); //print packet hex data
			  }
				cmd.data[i] = 'H';
		      Serial.println();
			newCommandFlag = 1;
		  }

		  Serial.println();


	  }
	  else if (xbee.getResponse().isError()) {
		  //nss.print("Error reading packet.  Error code: ");  
		  //nss.println(xbee.getResponse().getErrorCode());
		  // or flash error led
	  }
  }
	return cmd;
}

void xbeeAck(){
	 if(newCommandFlag){

	  //tx = Tx16Request(BASE_ADDRESS, ack, sizeof(ack));
      Serial.println("Sending Ack");
      xbee.send(txAck);

  
    // after sending a tx request, we expect a ack response
    // wait up to 5 seconds for the ack response
    if (xbee.readPacket(5000)) {
        // got a response!

        // should be a znet tx status            	
    	if (xbee.getResponse().getApiId() == TX_STATUS_RESPONSE) {
    	   xbee.getResponse().getTxStatusResponse(txStatus);
    		
    	   // get the delivery status, the fifth byte
           if (txStatus.getStatus() == SUCCESS) {
            	// success.  time to celebrate
             	//Serial.println("recieved transmit acknowledgment");
           } else {
            	// the remote XBee did not receive our packet. is it powered on?
             	Serial.println("did not receive tx Ack");
           }
        }      
    } else if (xbee.getResponse().isError()) {
      //nss.print("Error reading packet.  Error code: ");  
      //nss.println(xbee.getResponse().getErrorCode());
      // or flash error led
    } else {
      // local XBee did not provide a timely TX Status Response.  Radio is not configured properly or connected
      Serial.println("did not receive tx response!");
    }
    newCommandFlag = 0;
}
    delay(1000);
}
