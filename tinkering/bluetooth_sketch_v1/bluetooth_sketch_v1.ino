#include <Servo.h>

// Define pins and constants
#define ENA 5
#define ENB 11
#define IN1 6
#define IN2 7
#define IN3 8
#define IN4 9
#define carSpeed 250

Servo servo;
int rightDistance = 0, leftDistance = 0, middleDistance = 0;

enum FUNCTIONMODE {
  IDLE,
  Bluetooth,
  LineTeacking,
  ObstaclesAvoidance,
  IRremote
} func_mode = IDLE;

enum MOTIONMODE {
  STOP,
  FORWARD,
  BACK,
  LEFT,
  RIGHT
} mov_mode = STOP;

void forward(bool debug = false) {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  if (debug) Serial.println("Go forward!");
}

void back(bool debug = false) {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  if (debug) Serial.println("Go back!");
}

void left(bool debug = false) {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  if (debug) Serial.println("Go left!");
}

void right(bool debug = false) {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  if (debug) Serial.println("Go right!");
}

void stop(bool debug = false) {
  digitalWrite(ENA, LOW);
  digitalWrite(ENB, LOW);
  if (debug) Serial.println("Stop!");
}

void setup() {
  Serial.begin(9600); // Initialize serial communication
  servo.attach(3, 500, 2400); // Attach servo to pin 3 with pulse width limits
  servo.write(90); // Set initial servo position
  pinMode(IN1, OUTPUT); // Motor control pins
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'f': mov_mode = FORWARD;  break;
      case 'b': mov_mode = BACK;     break;
      case 'l': mov_mode = LEFT;     break;
      case 'r': mov_mode = RIGHT;    break;
      case 's': mov_mode = STOP;     break;
      default:  break;
    }
  }

  switch (mov_mode) {
    case FORWARD: forward();  break;
    case BACK:    back();     break;
    case LEFT:    left();     break;
    case RIGHT:   right();    break;
    case STOP:    stop();     break;
    default: break;
  }
}
