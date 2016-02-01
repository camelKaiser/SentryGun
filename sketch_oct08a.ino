int incomingByte = 0;
int ledPin = 13;
Servo myServo;
 
void setup(){
pinMode(ledPin, OUTPUT);
myServo.attach(4);
Serial.begin(9600);
}
 
void loop(){
 
if (Serial.available() > 0) 
{
// read the incoming byte:
incomingByte = Serial.read();
 
// say what you got:
     if(incomingByte == 1) 
     { // ASCII printable characters: 49 means number 1
          digitalWrite(ledPin, HIGH);
     } else if(incomingByte == 0){ // ASCII printable characters: 48 means number 0
          digitalWrite(ledPin, LOW);
     }
      else
     {
          myServo.write(incomingByte)
     }
}
 
 
}
 

