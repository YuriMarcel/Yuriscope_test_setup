const int Arrays = 4;
const int led_total = 16;
const int ledPins[Arrays][led_total] = {
  {5,4,15,16,7,2,14,3,6,8,12,17,9,10,11,13},              //1. array
  {22,18,27,26,21,19,29,30,20,23,31,28,24,25,33,32},      //3. array
  {44,45,49,48,42,47,46,38,43,41,37,35,40,39,36,34},      //4. array
  {A15,A13,A12,A11,A1,A14,A10,A8,A4,A2,A5,A9,A0,A3,A7,A6} //5. array
};

void setup() {
  Serial.begin(115200);

  // Initialise all pins
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 16; j++) {
      pinMode(ledPins[i][j], OUTPUT);
      digitalWrite(ledPins[i][j], LOW);  
    }
  }
}


void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();  // read comamnd from console
    command.trim();
    if (command.length() == 4) {
      int arrayID = command[0] - '0';  // convert char to int
      char ledState = command[1];
      int ledNumber = command.substring(2).toInt();
         
      if (command == "0000") {
        Serial.print("All LEDs off");
        turnAllLEDsOff();
        return;
      }
      // Array definition is shifted because Array 2 is connecteted to UNO
      switch (arrayID) {
        case 1: arrayID = 0; break;
        case 3: arrayID = 1; break;
        case 4: arrayID = 2; break;
        case 5: arrayID = 3; break;
      }

      controlLED(arrayID, ledState, ledNumber);
    }
  }
}

void controlLED(int arrayID, char state, int ledNum) {
  if (ledNum >= 1 && ledNum <= 16) {
    int pin = ledPins[arrayID][ledNum - 1];

    if (state == '1') {
      digitalWrite(pin, HIGH);
      Serial.print("LED on");
      
    } else if (state == '0') {
      digitalWrite(pin, LOW);
      Serial.print("LED on");
    }
  }
}

void turnAllLEDsOff() {
  for (int i = 0; i < Arrays; i++) {
    for (int j = 0; j < led_total; j++) {
      digitalWrite(ledPins[i][j], LOW);
    }
  }
}
