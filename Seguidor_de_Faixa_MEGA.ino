//Estou mexendo neste programa, ainda tem uns erros, precisamos ver se vamos precisar de um 3o sensor

#define sensorL 51
#define sensorR 50
#define trigPin 53
#define echoPin 52
#define motorL 5
#define motorR 3
#define motorLGND 4
#define motorRGND 2

int velocity = 0;
float distance = 0;
boolean count = true;

#define DELAY 2000

void setup() {
  pinMode(sensorL, INPUT);
  pinMode(sensorR, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorL, OUTPUT);
  pinMode(motorR, OUTPUT);
  
  pinMode(motorLGND, OUTPUT);
  pinMode(motorRGND, OUTPUT);
  digitalWrite(motorLGND, LOW);
  digitalWrite(motorRGND, LOW);
}

void followOutside() {
    if(digitalRead(sensorR) == 0){
      analogWrite(motorL, velocity);
      if(velocity == 200) analogWrite(motorR, 30);
      else analogWrite(motorR, velocity - 130);
    }
    else {
      if(velocity == 200) analogWrite(motorL, 30);
      else analogWrite(motorL, velocity - 130);
      analogWrite(motorR, velocity);
    }
}

void followInside() {
    if(digitalRead(sensorL) == 0) {
      if(velocity == 200) analogWrite(motorL, 30);
      else analogWrite(motorL, velocity - 130);
      analogWrite(motorR, velocity);
    }
    else {
      analogWrite(motorL, velocity);
      if(velocity == 200) analogWrite(motorR, 30);
      else analogWrite(motorR, velocity - 100);
    }
}

void ultrasonicRead() {
  float duration;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 58.2);
}

void stayAway() {
   if(distance < 25 && velocity > 130) {
      velocity--;
   }
   else {
      if(distance > 30 && velocity < 200) {
         velocity++;
      }
   }
}

void loop() {
  
  unsigned long time;
  
  ultrasonicRead();
  
  if(distance < 20) {  //Achou o Dummy
  
    stayAway();
    
    if(count) {  //Parte grande da trajetoria
      followInside();
      if(sensorR == 0) {
        velocity = 200;
        time = millis();
        while(millis() < time + DELAY) {
          followInside();
        }
        while(sensorR == 1) {
          followInside();
        }
        time = millis();
        while(millis() < time + DELAY) {
          followInside();
        }
      }
    }
    
    else {  //Parte pequena da trajetoria
      followOutside();
      if(sensorL == 0) {
        time = millis();
        while(millis() < time + DELAY) {
          stayAway();
          followOutside();
        }
        count = true;
      }    
    }
    
  }
  
  else {  //Nao achou o Dummy
  
    if(count) { //Parte grande da trajetoria
      velocity = 200;
      followOutside();
      if(sensorL == 0) {
        time = millis();
        while(millis() < time + DELAY) {
          followOutside();
        }
        count = false;
      }
    }   
    
    else { //Parte pequena da trajetoria
      velocity = 200;
      followOutside();
      if(sensorL == 0) {
        time = millis();
        while(millis() < time + DELAY) {
          followOutside();
        }
        count = true;
      }
    }
  }
}
