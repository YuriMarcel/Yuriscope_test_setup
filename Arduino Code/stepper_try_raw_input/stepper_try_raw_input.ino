#define stepPin_0 6
#define dirPin_0 5
#define stepPin_1 13
#define dirPin_1 12

#define SAFETY_SWITCH_0_PIN 18  // Ersetzen Sie X durch den tatsächlichen Pin
#define SAFETY_SWITCH_1_PIN 21  // Ersetzen Sie Y durch den tatsächlichen Pin


#define HOMING_SWITCH_0_PIN 2  // Ersetzen Sie durch den tatsächlichen Pin für Motor 0's Homing-Schalter
#define HOMING_SWITCH_1_PIN 20  // Ersetzen Sie durch den tatsächlichen Pin für Motor 1's Homing-Schalter

bool homingSwitch_0 = false;
bool homingSwitch_1 = false;
bool ignoreHomingSwitches = false;

volatile bool stopMotor_0 = false;
volatile bool stopMotor_1 = false;


volatile bool moveMotor = false;


//encoder 0
const int encoderPinA_0 = 3;
const int encoderPinB_0 = 10;

const int encoderPinA_1 = 19;
const int encoderPinB_1 = 11;

volatile int epos[] = {0, 0};

volatile int currentPos[] = {0, 0};

const int speed = 500;

void setup() {
  Serial.begin(115200);
  while (!Serial){
    ;
    }
  
  pinMode(SAFETY_SWITCH_0_PIN, INPUT_PULLUP);  // INPUT_PULLUP aktiviert den internen Pullup-Widerstand
  pinMode(SAFETY_SWITCH_1_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(SAFETY_SWITCH_0_PIN), stopMotor0_ISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(SAFETY_SWITCH_1_PIN), stopMotor1_ISR, FALLING);
  
  pinMode(stepPin_0, OUTPUT);
  pinMode(dirPin_0, OUTPUT);
  pinMode(stepPin_1, OUTPUT);
  pinMode(dirPin_1, OUTPUT);

    pinMode(encoderPinA_0, INPUT_PULLUP);
  pinMode(encoderPinB_0, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderPinA_0), updateEncoder_0, CHANGE);
  //  Set Max Speed and Acceleration of each Steppers at startup for homing

  pinMode(encoderPinA_1, INPUT_PULLUP);
  pinMode(encoderPinB_1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderPinA_1), updateEncoder_1, CHANGE);
  
  pinMode(HOMING_SWITCH_0_PIN, INPUT_PULLUP);  
  pinMode(HOMING_SWITCH_1_PIN, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(HOMING_SWITCH_0_PIN), homingSwitch0_ISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(HOMING_SWITCH_1_PIN), homingSwitch1_ISR, FALLING);




}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();  // Liest den Eingang
    command.trim();

    if (command.length() >= 2) {  // Mindestens 5 Zeichen (z.B. "85000")
      int motorId = command.substring(0, 1).toInt();
      int steps = command.substring(1).toInt();

      if (command == "start") {
      homing();
      return;  // Frühzeitig aus der Loop-Funktion zurückkehren, um andere Befehle zu ignorieren
    }
  
      switch(motorId) {
        case 8:
          moveToPosition(0, steps);
          break;
        case 9:
          moveToPosition(1, steps);
          break;
      }
    }
  }
}
void moveToPosition(int motorSelection, int targetPos) {
    ignoreHomingSwitches = true;
    moveMotor = true;

    int currentDifference = targetPos - currentPos[motorSelection];
    if (currentDifference == 0) {
      
      Serial.println("finished");
      moveMotor = false;
      
      return;
    }
    
    int dir = (currentDifference > 0) ? 1 : 0;
    int stepPin, dirPin;
    
    if (motorSelection == 0) {
        stepPin = stepPin_0;
        dirPin = dirPin_0;
    } else {
        stepPin = stepPin_1;
        dirPin = dirPin_1;
    }

    digitalWrite(dirPin, dir); // Setze die Richtung

    for (int x = 0; x < abs(currentDifference); x++) {
        //if ((motorSelection == 0 && stopMotor_0) || (motorSelection == 1 && stopMotor_1)) {
         // if ((motorSelection == 0 ) || (motorSelection == 1)) {
           // Serial.print("exit");
         //   break;
        //}

       
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
    }

    currentPos[motorSelection] = targetPos;
  
    Serial.println("finished");
    moveMotor = false;
    
    stopMotor_0 = false;
    stopMotor_1 = false;
    ignoreHomingSwitches = false;
}


void homing() {
  const int homingSpeed = 700;  // Mikrosekunden
      digitalWrite(dirPin_0, LOW);
      digitalWrite(dirPin_1, LOW);
      Serial.print(homingSwitch_0);
      Serial.print(homingSwitch_1);
  while (!homingSwitch_0 || !homingSwitch_1) {  // Während einer der Motoren nicht seinen Homing-Schalter erreicht hat
    if (!homingSwitch_0) {
      digitalWrite(stepPin_0, HIGH);
      delayMicroseconds(homingSpeed);
      digitalWrite(stepPin_0, LOW);
      delayMicroseconds(homingSpeed);
    }

    if (!homingSwitch_1) {
      digitalWrite(stepPin_1, HIGH);
      delayMicroseconds(homingSpeed);
      digitalWrite(stepPin_1, LOW);
      delayMicroseconds(homingSpeed);
    }
  }

  epos[0] = 0;
  epos[1] = 0;
  currentPos[0] = 0;
  currentPos[1] = 0;

  // Setzen Sie die Homing-Schalter-Flags zurück, um für das nächste Mal bereit zu sein
  homingSwitch_0 = false;
  homingSwitch_1 = false;

 // Bewegen Sie die Motoren zur Position 2000
 moveToPosition(1, 4000);
  while (true){
    if (moveMotor == false)break;
    }

 moveToPosition(0, 4000);
   while (true){
    if (moveMotor == false)break;
    }


  
  Serial.println("Homing completed!");


}




void stopMotor0_ISR() {
  stopMotor_0 = true;
  Serial.println("Safety Switch 0 activated");
}

void stopMotor1_ISR() {
  stopMotor_1 = true;
  Serial.println("Safety Switch 1 activated");
}
void updateEncoder_0() {
  if (digitalRead(encoderPinA_0) == digitalRead(encoderPinB_0)) {
    epos[0]+=8;
  } else {
    epos[0]-=8;
  }
}

void updateEncoder_1() {
  if (digitalRead(encoderPinA_1) == digitalRead(encoderPinB_1)) {
    epos[1]+=8;
  } else {
    epos[1]-=8;
  }
}
int homingSwitch0_ISR() {
  if (!ignoreHomingSwitches){
  homingSwitch_0 = true;
  Serial.println("Homeing 0 on");
  }
}

void homingSwitch1_ISR() {
  if (!ignoreHomingSwitches){
  homingSwitch_1 = true;
  Serial.println("Homeing 1 on");
  }
}
