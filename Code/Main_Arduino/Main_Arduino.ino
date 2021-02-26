// Connection to COM6 port on the computer 
// Opens/Closes door to allow receiving package
#include <Servo.h>
#include <SoftwareSerial.h>

#define OPEN 100
#define CLOSED 10

SoftwareSerial BTserial(2, 3); // RX | TX 
// Connect the HC-05 TX to Arduino pin 2 RX. 
// Connect the HC-05 RX to Arduino pin 3 TX through a voltage divider
Servo myservo;  

int n = 0;
int pos = 0;    // variable to store the servo position
char inByte = ' ';
 
void setup() 
{
    Serial.begin(9600);
    BTserial.begin(9600);  
    myservo.attach(9);  // attaches the servo on pin 9 to the servo object
    Serial.println("Arduino is ready");
    Serial.println("Remember to select Both NL & CR in the serial monitor");  
}
 
void loop()
{

  // send data only when you receive data:
  if (BTserial.available() > 0) {
    // read the incoming byte:
    inByte = BTserial.read();

    if(inByte == 'O'){
      //for(pos = CLOSED; pos < OPEN; pos += 1){
       //myservo.write(pos);              
       //Serial.println(inByte);
       //delay(5);
      //}     
       pos = OPEN;                   
       myservo.write(pos);                         
       Serial.println(inByte);
       delay(15);
    }
    if(inByte == 'C'){
       pos = CLOSED;
       myservo.write(pos);              
       Serial.println(inByte);
      delay(15);
    }
  }
}
