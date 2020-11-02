#include <Servo.h>
int servoPin = 2;
int servoPin2 = 3
int val = 0;
int IRPin = 5;  // LED connected to digital pin 13
int ledPin = 4;
int a = 22;  //For displaying segment "a"
int b = 23;  //For displaying segment "b"
int c = 24;  //For displaying segment "c"
int d = 25;  //For displaying segment "d"
int e = 26;  //For displaying segment "e"
int f = 27;  //For displaying segment "f"
int g = 28;  //For displaying segment "g"
int a2 = 29;  //For displaying segment "a"
int b2 = 30;  //For displaying segment "b"
int c2 = 31;  //For displaying segment "c"
int d2 = 32;  //For displaying segment "d"
int e2 = 33;  //For displaying segment "e"
int f2 = 34;  //For displaying segment "f"
int g2 = 35;  //For displaying segment "g"
int count = 0;

Servo servo;
Servo servo2;

void setup() {
  // put your setup code here, to run once:
  servo.attach(servoPin);
  servo2.attach(servoPin2);
  pinMode(IRPin, INPUT);
  pinMode(ledPin, OUTPUT);     
  pinMode(a, OUTPUT);  //A
  pinMode(b, OUTPUT);  //B
  pinMode(c, OUTPUT);  //C
  pinMode(d, OUTPUT);  //D
  pinMode(e, OUTPUT);  //E
  pinMode(f, OUTPUT);  //F
  pinMode(g, OUTPUT);  //G
  pinMode(a2, OUTPUT);  //A
  pinMode(b2, OUTPUT);  //B
  pinMode(c2, OUTPUT);  //C
  pinMode(d2, OUTPUT);  //D
  pinMode(e2, OUTPUT);  //E
  pinMode(f2, OUTPUT);  //F
  pinMode(g2, OUTPUT);  //G
  displayDigit(count);
}

void displayDigit(int digit)
{
    int Tens = digit / 10;
    int ones = digit % 10;
     //Conditions for displaying segment a
    if(ones!=1 && ones != 4)
    digitalWrite(a,HIGH);
    
    //Conditions for displaying segment b
    if(ones != 5 && ones != 6)
    digitalWrite(b,HIGH);
    
    //Conditions for displaying segment c
    if(ones !=2)
    digitalWrite(c,HIGH);
    
    //Conditions for displaying segment d
    if(ones != 1 && ones !=4 && ones !=7)
    digitalWrite(d,HIGH);
    
    //Conditions for displaying segment e 
    if(ones == 2 || ones ==6 || ones == 8 || ones==0)
    digitalWrite(e,HIGH);
    
    //Conditions for displaying segment f
    if(ones != 1 && ones !=2 && ones!=3 && ones !=7)
    digitalWrite(f,HIGH);
    if (ones!=0 && ones!=1 && ones !=7)
    digitalWrite(g,HIGH);
if (Tens != 0){
        if(Tens!=1 && Tens != 4)
    digitalWrite(a2,HIGH);
    
    //Conditions for displaying segment b
    if(Tens != 5 && Tens != 6)
    digitalWrite(b2,HIGH);
    
    //Conditions for displaying segment c
    if(Tens !=2)
    digitalWrite(c2,HIGH);
    
    //Conditions for displaying segment d
    if(Tens != 1 && Tens !=4 && Tens !=7)
    digitalWrite(d2,HIGH);
    
    //Conditions for displaying segment e 
    if(Tens == 2 || Tens ==6 || Tens == 8 || Tens==0)
    digitalWrite(e2,HIGH);
    
    //Conditions for displaying segment f
    if(Tens != 1 && Tens !=2 && Tens!=3 && Tens !=7)
    digitalWrite(f2,HIGH);
    if (Tens!=0 && Tens!=1 && Tens !=7)
    digitalWrite(g2,HIGH);
}
}
void turnOff()
{
  digitalWrite(a,LOW);
  digitalWrite(b,LOW);
  digitalWrite(c,LOW);
  digitalWrite(d,LOW);
  digitalWrite(e,LOW);
  digitalWrite(f,LOW);
  digitalWrite(g,LOW);
  digitalWrite(a2,LOW);
  digitalWrite(b2,LOW);
  digitalWrite(c2,LOW);
  digitalWrite(d2,LOW);
  digitalWrite(e2,LOW);
  digitalWrite(f2,LOW);
  digitalWrite(g2,LOW);
}
void motorRun(){
  servo.write(120);
  delay(2000);
  servo.write(30);
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  servo.write(90);
  delay(1000);
  servo.write(0);
  delay(2000);
  printf(servo.read());
  */
  val = digitalRead(IRPin);
  if (val == LOW) {
   digitalWrite(ledPin, HIGH);
   turnOff();
   displayDigit(count);
   motorRun();
   delay(1000);
   count += 1;
   if (count == 100){
    count = 0;
   }
    /*
    digitalWrite(ledPin, HIGH);
    servo.write(90);
    delay(100);
    servo.write(0);
    delay(100);
    */
  } else {
    digitalWrite(ledPin, LOW);
  }
}