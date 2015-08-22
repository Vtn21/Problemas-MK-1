#define sensorL 1
#define sensorR 8
#define trigPin 11
#define echoPin 3
#define motorL 9
#define motorR 6
#define motorLGND 10
#define motorRGND 5

int distance, velocity,
    *ptr_vel = &velocity;
boolean count;

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
  
  pinMode(2, OUTPUT); //Gambiarra a ser corrigida
  digitalWrite(2, HIGH);

}

void followOutside(int velocity) {
    if(digitalRead(sensorR) == 1) {
      analogWrite(motorL, velocity);
      analogWrite(motorR, velocity - 150);
    }
    else {
      analogWrite(motorL, velocity - 150);
      analogWrite(motorR, velocity);
    }
}

void followInside(int velocity) {
    if(digitalRead(sensorL) == 1) {
      analogWrite(motorL, velocity - 150);
      analogWrite(motorR, velocity);
    }
    else {
      analogWrite(motorL, velocity);
      analogWrite(motorR, velocity - 150);
    }
}

float ultrasonicRead() {
  float duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;
  return distance;
}

void stayAway(int *velocity) {
   if(ultrasonicRead() < 10) {
      if(*velocity > 0) (*velocity)--;
   }
   else {
      if(distance > 15) {
         if(*velocity < 255) (*velocity)++;
      }
   }
}

void loop() {
  
  if(ultrasonicRead() < 20) {  //Achou o Dummy
  
    stayAway(ptr_vel);
    
    if(count) {  //Parte grande da trajetoria
      followInside(velocity);
      if(sensorR == 1) {
        velocity = 150;
        while(sensorR == 1) {
          followInside(velocity);
        }
        while(sensorR == 0) {
          followInside(velocity);
        }
        while(sensorR == 1) {
          followInside(velocity);
        }
      }
    }
    
    else {  //Parte pequena da trajetoria
      followOutside(velocity);
      if(sensorL == 1) {
        while(sensorL == 1) {
          stayAway(ptr_vel);
          followOutside(velocity);
        }
        count = true;
      }    
    }
    
  }
  
  else {  //Nao achou o Dummy
  
    if(count) {
      velocity = 255;
      followOutside(velocity);
      if(sensorL == 1) {
        while(sensorL == 1) {
          followOutside(velocity);
        }
        count = false;
      }
    }   
    
    else {
      velocity = 255;
      followOutside(velocity);
      if(sensorL == 1) {
        while(sensorL == 1) {
          followOutside(velocity);
        }
        count = true;
      }
    }
    
  }
  
}
