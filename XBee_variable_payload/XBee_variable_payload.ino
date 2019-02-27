
const unsigned char PacketLength = 30;
unsigned char Packet1[PacketLength];
int led = 13;
unsigned char PayloadStart;
unsigned char PayloadEnd;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial1.begin(9600);
  pinMode(13,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13,LOW);
  for(int x=0; x<PacketLength; x++){
    Packet1[x] = 0x00;
  }

  Serial.println(" ");
  for(int x=0; x<PacketLength; x++){
    Serial.print(Packet1[x],HEX);
    Serial.print(" ");
    delay(10);
  }
  Serial.println(" ");
  while(Serial1.available() == 0){}

  for(int x=0; x<PacketLength; x++){
    Packet1[x] = Serial1.read();
    delay(10);
  }
  
  for(int x=0; x<PacketLength; x++){
    Serial.print(Packet1[x],HEX);
    Serial.print(" ");
  }
  Serial.println(" ");

  PayloadStart = 8;
  PayloadEnd = 0;

  while(Packet1[PayloadEnd] < 0xFF){
    PayloadEnd++;
  }
  PayloadEnd = PayloadEnd-1;
  Serial.print("Payload: ");
  for(int x=PayloadStart; x<PayloadEnd; x++){
    Serial.print(Packet1[x],HEX);
    Serial.print(" ");
  }
  Serial.println(" ");
  digitalWrite(13,HIGH);
  delay(1000);
  }
  
