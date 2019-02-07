/*
  ServoSequence
  Reads an analog input, and plays different servo sequences depending on the analog value
 
  This example code is in the public domain.
 */
#include "TimerOne.h"
#include "VarSpeedServo.h"
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  150 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // this is the 'maximum' pulse length count (out of 4096)

int val=0;
// Variable zum Speichern der Position
int pos = 0;
int i = 0;
int pos1=90;
int spd=90;
int w = 0;
char input[7];

VarSpeedServo myservo1;
VarSpeedServo myservo2;

const int servoPin1 = 10;  // the digital pin used for the servo
const int servoPin2 = 9;

const int readpin = 4; 



// the setup routine runs once when you press reset:
void setup() { 
  myservo1.attach(servoPin1,900,2100);
  myservo1.write(0,115,true);
//  myservo2.attach(servoPin2);
//  myservo2.write(0);
 // pinMode(3, INPUT); 
  
  //Timer1.initialize(1*100000);
  //Timer1.attachInterrupt(timer1);
  Serial.begin(9600);

   // myservo1.write(180,5, true); 
    
//    pwm.begin();
//    pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
//    yield();
}

// the loop routine runs over and over again forever:
void loop() {


        myservo1.write(180,10, true); 
        //delay(2500);
        myservo1.write(0,60, true); 
        //delay(2500);
   
//  #define INPUT_SIZE 11
//    
//    while (Serial.available() == 0); {
//      // Get next command from Serial (add 1 for final 0)
//      char input[INPUT_SIZE + 1];
//      byte size = Serial.readBytes(input, INPUT_SIZE);
//      // Add the final 0 to end the C string
//      //input[size] = 0;
//
//      String input_str = input;
//      pos1 = input_str.substring(0,3).toInt();
//      spd = input_str.substring(4,7).toInt();
//      w = input_str.substring(8,9).toInt();
//      Serial.println("");
//      Serial.println(pos1);
//      Serial.println(spd);
//      Serial.println(w);
//      if (w == 1) { 
//        //pwm.setPWM(pos1, 0, 650);
//        myservo1.write(pos1,spd, true); 
//      }
//      if (w == 0) { 
//        //pwm.setPWM(pos1, 0, 150);
//        myservo1.write(pos1,spd, false); 
//      }
//   }   
                            //  alt
                      ////      char* pos = strtok (input," ,");
                      ////          
                      ////            Serial.println(input);
                      ////          pos1 = atoi(pos);
                      ////          //Serial.println(pos1);
                      ////          pos = strtok (NULL," ,");
                      ////          pos2 = atoi(pos);
                      ////          Serial.println(pos2);
                      ////          if (pos1 == 0) { myservo1.write(myservo1.read()); myservo1.stop(); }
                      ////          else {
                      ////            fahre(pos1, pos2);
                      ////            
                      ////          //Serial.println(myservo1.read());
                      ////          //Serial.println(myservo1.write(pos1,pos2,true));
                      ////          }
                         // }

  
}

void fahre(int a, int b) {
  myservo1.write(a,b, false);
  
 // myservo1.stop();
          //myservo1.write(30,100, true);
}



void timer1() {
   if (pos1 == 0) { myservo1.stop(); }  
}
