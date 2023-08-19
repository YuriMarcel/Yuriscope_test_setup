const int ledPins[] = {12,10,9,6,13,11,7,5,8,A1,A0,4,A3,A2,3,2};

void setup() {
  Serial.begin(115200);

  // Initialise all Pins
  for (int i = 0; i < 16; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  
  }

}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();  // read input
    command.trim();

    if (command.length() == 4) {
      char arrayID = command[0];
      char ledState = command[1];
      int ledNumber = command.substring(2).toInt();

        if (command == "0000") {
        turnAllLEDsOff();
        Serial.print("All LEDs off");
        return;
      }
      
      if (arrayID == '2') {  // only used second Array
        controlLED(ledState, ledNumber);
      }
    }
  }
}

void controlLED(char state, int ledNum) {
  if (ledNum >= 1 && ledNum <= 16) {
    int pin = ledPins[ledNum - 1];

    if (state == '1') {
      digitalWrite(pin, HIGH);
      Serial.print("LED on");
    } else if (state == '0') {
      digitalWrite(pin, LOW);
      Serial.print("LED off");
    }
  }
}

void turnAllLEDsOff() {
  for (int i = 0; i < 16; i++) {    
      digitalWrite(ledPins[i], LOW);
  }
}
