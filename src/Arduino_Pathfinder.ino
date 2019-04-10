//Main Pathfinder Program


#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Wire.h>
#include <Printers.h>
#include <XBee.h>
#include <Robot.h>


/* Assign a unique ID to this sensor at the same time */
Adafruit_LSM303_Mag_Unified mag = Adafruit_LSM303_Mag_Unified(12345);
const int NUMBER_OF_FIELDS = 30;  //how many comma seperated fields we expect
int fieldIndex = 0;               // the currect field being recieved
//unsigned int MissionPath[NUMBER_OF_FIELDS];  // Array holding values for all the fields
//unsigned int MissionPath [] = {1, 100, 3, 0, 1, 50, 4, 0};
unsigned int x = 0;
float headingDegrees;
int StartHeading, CurrentHeading;
int TurnAngleAmount = 90;

struct Path
{
  uint8_t command;
  uint8_t distance;
};

struct Path MissionPath[30];
int MissionSize = 0;


int RFSpd = 200; //Right Motor Forward Speed
int RRSpd = -200; //Right Motor Reverse Speed
int LFSpd = 200; //Left Motor Forward Speed
int LRSpd = -200; //Left Motor Reverse Speed
int LStop = 0;  //Left Motor Stop
int RStop = 0;  //Right Motor Stop

int i;
//--------------------------------------------------------

XBee xbee = XBee();

Rx16Response rx16 = Rx16Response();
const int BASE_ADDRESS = 0x0036;

bool newCommandFlag = 0;


// 16-bit addressing: Enter address of remote XBee, typically the coordinator
uint8_t ack[] = { 0, 0, 0 }; //ack is {command, distance, completed} echoes command and says if completed
uint8_t coords[] = {0, 0, 0, 0};

Tx16Request txAck = Tx16Request(BASE_ADDRESS, ack, sizeof(ack));
Tx16Request txCoords = Tx16Request(BASE_ADDRESS, coords, sizeof(coords));
TxStatusResponse txStatus = TxStatusResponse();

uint8_t option = 0;
struct commands {
  uint8_t data[30];
};

commands xbeeReceive();
void xbeeAck();
//void xbeeSendCoords();

void setup (void) {
  Initialize();
  Stop();
}

void loop()
{
  commands commandArray = commands();
  commandArray = xbeeReceive();
  if(newCommandFlag){
    GetMissionPath(commandArray);
    ExecutePath();
  }
  ack[0] = commandArray.data[0];
  ack[1] = commandArray.data[1];
  ack[2] = 1;
  xbeeAck();
}
void Forward(unsigned int RunTime)
{
  Serial.println("Made it to here");
  GetHeading();
  Serial.print("StartHeading (degrees) : ");
  Serial.println(headingDegrees);
  StartHeading = (int)headingDegrees;
  rightMotor.setSpeed(RFSpd);
  //Left Track Constant Speed
  while ( RunTime > 0) //Adjust the left wheel for steering
  {
    GetHeading();
    Serial.print("CurrentHeading (degrees) : ");
    Serial.println(headingDegrees);
    CurrentHeading = (int)headingDegrees;
    if (CurrentHeading == StartHeading)
    {
      leftMotor.setSpeed(LFSpd);
      Serial.println("Go Straight");
      delay(200);

    }
    if (CurrentHeading > StartHeading + 5)
    {
      rightMotor.setSpeed(RFSpd);
      Serial.println("Veer Left");
      delay(200);
    }
    if (CurrentHeading < StartHeading - 5)
    {
      leftMotor.setSpeed(LFSpd);
      Serial.println("Veer Right");
      delay(200);
    }
    RunTime--;
  }
  Stop();
  delay(2000);
}
void Reverse(unsigned int RunTime)
{
  GetHeading();
  rightMotor.setSpeed(RRSpd);
  leftMotor.setSpeed(LRSpd);
  delay(RunTime);
  Stop();
  delay(2000);
}
void TurnRight(unsigned int RunTime)
{
  GetHeading();
  StartHeading = (int)headingDegrees;
  CurrentHeading = (int)headingDegrees;
  while (CurrentHeading < (StartHeading + TurnAngleAmount))
  {
    rightMotor.setSpeed(RRSpd);
    leftMotor.setSpeed(LFSpd);
    delay(100);
    Serial.println("Keep Turning Right");
    GetHeading();
    CurrentHeading = (int)headingDegrees;
    Serial.print("StartHeading: "); Serial.println(StartHeading);
    Serial.print("   CurrentHeading:  "); Serial.println(CurrentHeading);
  }
  Stop();
  delay(2000);
}
void TurnLeft(unsigned int RunTime)
{
  GetHeading();
  StartHeading = (int)headingDegrees;
  CurrentHeading = (int)headingDegrees;
  while ( CurrentHeading > (StartHeading - TurnAngleAmount + 8) )
  {
    rightMotor.setSpeed(RFSpd);
    leftMotor.setSpeed(LRSpd);
    delay(100);
    Serial.println("Keep Turning Left");
    GetHeading();
    CurrentHeading = (int)headingDegrees;
    Serial.print("StartHeading: "); Serial.print(StartHeading);
    Serial.print("   CurrentHeading:  "); Serial.println(CurrentHeading);
  }
  Stop();
  delay(2000);
}
void  Stop(void)
{
  rightMotor.setSpeed(RStop);
  leftMotor.setSpeed(LStop);
}
void GetHeading(void)
{
  //Get a New sensor event
  sensors_event_t event;
  mag.getEvent(&event);

  //Hold the module so that z is pointing 'up' and you can measure the heading with x&y
  //Calculate heading when the magnetometer is level, then correct for signs of axis
  float heading = atan2(event.magnetic.y, event.magnetic.x);

  //Once you have your heading, you must then add your 'Declination Angle', which is the 'Error' of the magnetic field of your location
  //Find yours here: https//www.magnetic-declination.com
  //If you cannot find your Declination, comment out these two lines, your compass will be slightly off.
  float declinationAngle = 0.17;
  heading += declinationAngle;

  //Correct for when signs are reversed.
  if (heading < 0)
    heading += 2 * PI;

  //Check for wrap due to addition of declination.
  if (heading > 0)
    heading -= 2 * PI;


  //Convert radians to degrees for readability.
  headingDegrees = heading * 180 / M_PI;

  Serial.print("Heading (degrees): "); Serial.println(headingDegrees);

}
void Initialize(void)
{
  Serial.begin(9600);
  Serial1.begin(9600);
  mag.begin();
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  xbee.setSerial(Serial1);
}
commands xbeeReceive() {
  commands cmd = commands();
  xbee.readPacket();
  if (xbee.getResponse().isAvailable()) {
    // got something
    Serial.println("received communication");
    //for (int i = 0; sizeof(data); i++) {
    //  data[i] = 0;
    //}

    if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
      // got a rx packet

      if (xbee.getResponse().getApiId() == RX_16_RESPONSE) {
        Serial.println("16 bit response received");
        xbee.getResponse().getRx16Response(rx16);
        option = rx16.getOption();
        int i = 0;
        for (i = 0; i < rx16.getDataLength(); i++) {
          cmd.data[i] = rx16.getData(i);
          Serial.print(F("0x")); Serial.print(cmd.data[i], HEX); Serial.print(" "); //print packet hex data
        }

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
void xbeeAck() {
  if (newCommandFlag) {

    //tx = Tx16Request(BASE_ADDRESS, ack, sizeof(ack));
    xbee.send(txAck);


    // after sending a tx request, we expect a status response
    // wait up to 5 seconds for the status response
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
  delay(200);
}
void GetMissionPath(commands rawCommands)
{
  const char COMMAND_START = 2;
  int i = COMMAND_START; //first two bytes are the number of the command
  int pathNum = 0; //current path command we're on
  while (rawCommands.data[i] != 0x48) {
    pathNum = (i-COMMAND_START) / 2;
    if (pathNum > 30) {
      break;
    }

    if (i % 2 == 0) {
      MissionPath[pathNum].command = rawCommands.data[i];
    }
    else {
      MissionPath[pathNum].distance = rawCommands.data[i];
    }
    i++;
  }
  MissionSize = pathNum + 1;
  
  for(i = 0; i < MissionSize; i++){
    Serial.print("Command: " + String(MissionPath[i].command) + " ");
    Serial.print("Distance: " + String(MissionPath[i].distance));
    Serial.println();
  }

}
void ExecutePath ()
{
    for (int i = 0;i<MissionSize;i++)
    {
      switch(MissionPath[i].command){
        case 1:
          Serial.print("Going Forward");
          Forward(MissionPath[i].distance);
          break;
        case 2:
          Serial.print("Turning Right");
          TurnRight(100);
          break;
        case 3:
          Serial.print("Turning Left");
          TurnLeft(100);
          break;
        default:
          break;
      }
      
    }
}
/*GetMissionPath();
   Serial.println("Made it to here");
    while(x<NUMBER_OF_FIELDS)
    {

      if(MissionPath[x] == 1) {Forward(MissionPath[x+1]); }
      if(MissionPath[x] == 2) {Reverse(MissionPath[x+1]); }
      if(MissionPath[x] == 3) {TurnRight(MissionPath[x+1]); }
      if(MissionPath[x] == 4) {TurnLeft(MissionPath[x+1]); }
      x++;
      x++;
    }
   while(1){}
   delay(500);
*/
/*void GetMissionPath(void)
  {
  while (Serial1.available() == 0){}
  while (MissionPath[i] != 'H')
  {
       if (Serial1.available())
       {
             char ch = Serial1.read();
             if (ch >= '0' && ch <= '9') // is this an ascii digit between 0 and 9?
             {
                   //yes, accumulate the value if the fieldIndex is within range
                   // addition fields are not stored
                   if (fieldIndex < NUMBER_OF_FIELDS)
                   {
                         MissionPath[fieldIndex] = (MissionPath[fieldIndex] * 10) +
                         (ch - '0');
                   }

             }
             else if (ch == ',') // comma is our separator, so move on to the next field
             {
              fieldIndex++;  //increment field index
             }
             else
             {
                  // any character not a digit or comma ends the aquisition of fields
                  // in this example it's the newline character sent by the Serial Monitor
                  // Print each of the stored fileds
                  for(int i=0; i < min(NUMBER_OF_FIELDS, fieldIndex+1); i++)
                  {
                    Serial.println(MissionPath[i]);
                  }
                  break;
             }
       }
  }
       Serial.println("Ok, received the commands");
  }*/
