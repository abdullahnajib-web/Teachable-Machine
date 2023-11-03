#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>


LiquidCrystal_I2C lcd(0x20, 16, 2);
Servo servo;
int pinBuzzer = 5;

byte result = 255;


void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();

  servo.attach(3);
  pinMode(pinBuzzer, OUTPUT);
}
byte last = 0;
void loop() {
  // read a single byte from serial port
  if (Serial.available() > 0) {
    result = Serial.read();

    if (last != result) {

      // LCD
      lcd.clear();
      if (result == 10) {
        lcd.print("Shield");
      } else if (result == 11) {
        lcd.print("Neopixel");
      } else if (result == 12) {
        lcd.print("-");
      } else if (result == 13) {
        lcd.print("Wheel");

        // Servo
      } else if (result == 0) {
        servo.write(0);
      } else if (result == 1) {
        servo.write(180);

        // Buzzer
      } else if (result == 3) {
        tone(pinBuzzer, 261);
        delay(200);
        noTone(pinBuzzer);
        result = 255;
      } else if (result == 4) {
        tone(pinBuzzer, 349);
        delay(200);
        noTone(pinBuzzer);
        result = 255;
      } else if (result == 5) {
        tone(pinBuzzer, 500);
        delay(200);
        noTone(pinBuzzer);
        result = 255;
      }
    }
    last = result;

    while (Serial.available() > 0) {
      Serial.read();
    }

  }
}
