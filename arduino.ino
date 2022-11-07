#include <Servo.h>//舵机
//Servo myservo;     //控制门的舵机
int pos = 0;            //  初始化舵机位置

void setup()
{
Serial.begin(9600);     //esp-8266
myservo.attach(9);      //门舵机控制9
myservo.write(0); //初始化门舵机
delay(10000);
}

void loop() {  
  
  while(mySerial.available())  //如果串口可用
   {  char c;
      c=Serial.read();
      Serial.println (c);
      switch(c){
        case '1':servo_init();
        break;
        case '2':open_the_door();
        break;
        case '3':close_the_door();
        break;
	default:servo_init();     
               }
   }
}
void servo_init()
{
	myservo.write(0);
	delay(1000);
}

void open_the_door()
{
	for (pos = 0; pos <= 180; pos +=1) {
	myservo.write(pos);
	delay(5);
}
}

void close_the_the_door()
{
	for (pos = 180; pos >= 0; pos -=1) {
	myservo.write(pos);
	dealy(5);
}
}