#include "AccelStepper.h"
// Library created by Mike McCauley at http://www.airspayce.com/mikem/arduino/AccelStepper/

// AccelStepper Setup
#define stepPin_0 6
#define dirPin_0 5

#define stepPin_1 13
#define dirPin_1 12


AccelStepper stepper0(1, stepPin_0, dirPin_0);   // 1 = Easy Driver interface
AccelStepper stepper1(1, stepPin_1, dirPin_1);

AccelStepper* steppers[2] = {
  &stepper0,
  &stepper1,
};

// Define the Pins used
#define home_switch_0 2 // Pin 2 connected to Home Switch (MicroSwitch)
#define saftey_switch_0 18

#define home_switch_1 20
#define saftey_switch_1 21
// Stepper Travel Variables
int move_finished = 1; // Used to check if move is completed
long initial_homing = 1; // Used to Home Stepper at startup
int error = 1;

//encoder 0
const int encoderPinA_0 = 3;
const int encoderPinB_0 = 10;

const int encoderPinA_1 = 19;
const int encoderPinB_1 = 11;

volatile int epos[] = {0, 0};

int x = 0, w, distance;
int button_state;

void setup() {

  Serial.begin(115200);  // Start the Serial monitor with speed of 9600 Bauds

  pinMode(home_switch_0, INPUT_PULLUP);
  pinMode(saftey_switch_0 , INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(saftey_switch_0), Saftey_0, CHANGE);

  pinMode(home_switch_1, INPUT_PULLUP);
  pinMode(saftey_switch_1 , INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(saftey_switch_1), Saftey_1, CHANGE);


  delay(2000);  // Wait for EasyDriver wake up

  //encoder setup
  pinMode(encoderPinA_0, INPUT_PULLUP);
  pinMode(encoderPinB_0, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderPinA_0), updateEncoder_0, CHANGE);
  //  Set Max Speed and Acceleration of each Steppers at startup for homing

  pinMode(encoderPinA_1, INPUT_PULLUP);
  pinMode(encoderPinB_1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderPinA_1), updateEncoder_1, CHANGE);

}
void loop() {

  if (Serial.available() > 0)  { // Check if values are available in the Serial Buffer

    move_finished = 0; // Set variable for checking move of the Stepper
    String TravelX = Serial.readStringUntil('\n');

    if (TravelX == "start") {
      Serial.println("Homeing process started!");
      epos[0]=homeing(home_switch_0,0);
      epos[1]=homeing(home_switch_1,1);
      
      Serial.print("The encoder_0 is at position:   "); Serial.println(epos[0]);
      Serial.print("The encoder_1 is at position:   "); Serial.println(epos[1]);
      Serial.println("Homing Completed    ");
      Serial.print("x");
    }

    //Serial.print(TravelX);
    w = (TravelX.substring(0, 1)).toInt();
    distance = (TravelX.substring(1, 5)).toInt();

    switch (w) {
      case 8:
        steppers[0]->moveTo(distance);  // Set new moveto position of Stepper
        delay(100);
        Serial.print("Moving stepper 2 into position: ");
        Serial.println(distance);
        break;

      case 9:
        steppers[1]->moveTo(distance);  // Set new moveto position of Stepper
        delay(100);
        Serial.print("Moving stepper 1 into position: ");
        Serial.println(distance);
        break;
    }
  }


  switch (w) {
    case 8:
      moveStepper(0, distance, epos);
      break;

    case 9:
      moveStepper(1, distance, epos);
      break;
  }

}
void updateEncoder_0() {
  if (digitalRead(encoderPinA_0) == digitalRead(encoderPinB_0)) {
    epos[0]+=4;
  } else {
    epos[0]-=4;
  }
}

void updateEncoder_1() {
  if (digitalRead(encoderPinA_1) == digitalRead(encoderPinB_1)) {
    epos[1]+=4;
  } else {
    epos[1]-=4;
  }
}

int homeing(int home_switch, int i) {
  steppers[i]->setMaxSpeed(200);
  steppers[i]->setAcceleration(100.0);
  while (digitalRead(home_switch)) { // Make the Stepper move CCW until the switch is activated
    steppers[i]->moveTo(initial_homing);  // Set the position to move to
    initial_homing--;  // Decrease by 1 for next move if needed
    steppers[i]->run();// Start moving the stepper
    delay(2);
  }
  steppers[i]->setCurrentPosition(0);  // Set the current position as zero for now
  initial_homing = -1;
  return 0;
}

int moveStepper(int i, int d, volatile int ary[]) {

  if ((steppers[i]->distanceToGo() != 0)) { // Check if the Stepper has reached desired position
    steppers[i]->run();  // Move Stepper into position
  }

  if ((move_finished == 0) && (steppers[i]->distanceToGo() == 0)) {
    delay(500);
    error = ary[i] - d;

    if ((error != 0)) {
      Serial.println("DEVIATION");
      delay(500);
      Serial.print("The encoder before correction:   ");
      Serial.println(ary[i]);
      int j = 1;
      while (error != 0) {
        delay(100);
        steppers[i]->move(-error);
        steppers[i]->run();
        delay(50);
        Serial.println(j);
        j++;
        error = ary[i] - d;
      }

      Serial.print("The encoder after correction:   ");
      Serial.println(ary[i] );
      steppers[i]->setCurrentPosition(ary[i]);
      Serial.print("x");
      error = 0;
      move_finished = 1;
    }
    else {

      Serial.println("COMPLETED and NO DEVIATION!" );
      Serial.print("The encoder is at position:  ");
      Serial.println(ary[i]);
      Serial.print("x");
      move_finished = 1; // Reset move variable
    }
  }

  return 0;
}


void Saftey_0() {
  if (digitalRead(saftey_switch_0)) {
    Serial.println("Safety Switch 0 activated");
    stepper0.moveTo(0);  // Set new moveto position of Stepper
    distance = 0;
    delay(100);  // Wait 1 seconds before moving the Stepper
    if ((stepper0.distanceToGo() != 0)) {
      stepper0.run();  // Move Stepper into position
    }
  }
}
void Saftey_1() {
  if (digitalRead(saftey_switch_1)) {
    Serial.println("Safety Switch 1 activated");
    stepper1.moveTo(0);  // Set new moveto position of Stepper
    distance = 0;
    delay(100);  // Wait 1 seconds before moving the Stepper
    if ((stepper1.distanceToGo() != 0)) {
      stepper1.run();  // Move Stepper into position
    }
  }
}
