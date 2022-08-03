#include <Servo.h>

// PINOUT
// + Ultrsonic
#define ECHO_PIN 9
#define TRIGGER_PIN 8
// + Servo
#define SERVO_PIN 10
// + Motors
// Speed Control
#define E1 4  
#define E2 7
// Direction Control     
#define M1 5    
#define M2 6
// + Communications with esp32 (wifi connection)
// Commands 1-5
#define COMMAND1 A0
#define COMMAND2 A1
#define COMMAND3 A2
#define COMMAND4 A3
#define COMMAND5 A4
// Read ACK to esp32
#define READ_FINISH A5

// CONSTANTS
// + Distance threshold to define if there is obstacle
#define THRESHOLD 25
// + Time (ms) to travel 1 grid cell
#define FORWARD_TIME 2000
// + Time (ms) to turn left or rigth
#define TURN_TIME 550
// + Time (ms) to turn back
#define TURN_BACK_TIME 1100
// + Time to wait the servo to arrive to the target position
#define TIME_SERVO_TARGET 1000


// Variable that contains the initial orientation of the robot -> 1 = top, 2 = left, 3 = bot, 4 = right
int robotOrientation = 3;

Servo myservo;

void setup(){
   Serial.begin(9600);
   pinMode(TRIGGER_PIN, OUTPUT);
   pinMode(ECHO_PIN, INPUT);
   myservo.attach(SERVO_PIN);
   
   pinMode(READ_FINISH, OUTPUT);
   pinMode(COMMAND1, INPUT);
   pinMode(COMMAND2, INPUT);
   pinMode(COMMAND3, INPUT);
   pinMode(COMMAND4, INPUT);
   pinMode(COMMAND5, INPUT);

   pinMode(E1, OUTPUT);
   pinMode(E2, OUTPUT);
   pinMode(M1, OUTPUT);
   pinMode(M2, OUTPUT); 
}

void loop(){
   getCommand();
   delay(100);
}

void getCommand(){
  // Read pins and call corresponding command
  // 1 = top, 2 = left, 3 = bot, 4 right
  // 5 = check3Directions
  int state = 0;
  if(digitalRead(COMMAND1)){
    moveRobot(1);
    state = COMMAND1;
  }else if(digitalRead(COMMAND2)){
    moveRobot(2);
    state = COMMAND2;
  }else if(digitalRead(COMMAND3)){
    moveRobot(3);
    state = COMMAND3;
  }else if(digitalRead(COMMAND4)){
    moveRobot(4);
    state = COMMAND4;
  }else if(digitalRead(COMMAND5)){
    check3Directions();
    state = COMMAND5;
  }

  // Indicate to the wifi module that operation is finished and wait to turn of signals
  if(state != 0){
    digitalWrite(READ_FINISH, HIGH); 
    while(digitalRead(state)){
      delay(100);
    }
    digitalWrite(READ_FINISH, LOW);
  }
}

int getDistance(){
   // Generate the init pulse
   digitalWrite(TRIGGER_PIN, LOW); 
   delayMicroseconds(4);
   digitalWrite(TRIGGER_PIN, HIGH);
   delayMicroseconds(10);
   digitalWrite(TRIGGER_PIN, LOW);
   
   // Get input pulse and calculate distance
   return pulseIn(ECHO_PIN, HIGH) * 10 / 292/ 2;
}

bool checkObstacle(){
  bool obstacle = false;
  if(getDistance() < THRESHOLD){
    obstacle = true;
  }
  return obstacle;
}

void check3Directions(){
  int state;
  // Move ultrasonic to left
  myservo.write(0);
  delay(TIME_SERVO_TARGET);
  // Check left
  if(checkObstacle()){
    state = 6;
  }else{
    state = 5;
  }
  // Send state to app
  sendState(state);

  // Move ultrasonic to front
  myservo.write(90);
  delay(TIME_SERVO_TARGET);
  // Check front
  if(checkObstacle()){
    state = 6;
  }else{
    state = 5;
  }
  // Send state to app
  sendState(state);

  // Move ultrasonic to right
  myservo.write(180);
  delay(TIME_SERVO_TARGET);
  // Check right
  if(checkObstacle()){
    state = 6;
  }else{
    state = 5;
  }
  // Send state to app
  sendState(state);
}

void DriveMotorP(boolean forward1, boolean forward2, byte m1p, byte m2p){
  // Controll motor movement
  digitalWrite(E1, forward1);
  analogWrite(M1, (m1p));

  digitalWrite(E2, forward2); 
  analogWrite(M2, (m2p));
}

int globalCommand2localCommand(int globalCommand){
  // Convert a global command (superior view of grid map) to local movement and change robot orientation
  // global commands: 1 = top, 2 = left, 3 = bot, 4 right
  // local commands: 1 = fordward, 2 = left, 3 = back, 4 right
  int localMovement = -1;
  
  if(globalCommand == robotOrientation){
    // If match, they are in the same direction
    localMovement = 1;
  }else if(globalCommand+2%4 == robotOrientation){
    // Turn back if they are complementary in module 4 (num commands)
    localMovement = 3;
  }else if(robotOrientation-1%4 == globalCommand){
    // Turn right if robot orientation - 1 == global command (it means if it is necessary to turn right)
    localMovement = 4;
  }else{
    // Turn left in other cases
    localMovement = 2;
  }
  // Change the robot orientation to the new command
  robotOrientation = globalCommand;
  return localMovement;
}

void moveRobot(int command){
  // Transform global command to local movement
  command = globalCommand2localCommand(command);
  if(command == 1){
    // FORWARD
    DriveMotorP(true, true, 0x7f, 0x7f);
    delay(FORWARD_TIME);
  }else if(command >= 2 && command <= 4){
    // Turn to the correct direction
    if(command == 2){
      // LEFT
      DriveMotorP(false, true, 0x7f, 0x7f);
      delay(TURN_TIME);
    }else if(command == 3){
      // BACK
      DriveMotorP(true, false, 0x7f, 0x7f);
      delay(TURN_BACK_TIME);
    }else if(command == 4){
      // RIGHT
      DriveMotorP(true, false, 0x7f, 0x7f);
      delay(TURN_TIME);
    }
    // Advance 1 cell
    DriveMotorP(true, true, 0x7f, 0x7f);
    delay(FORWARD_TIME);
  }
  // Turn off motors
  DriveMotorP(false, false, 0x0, 0x0);
}

void sendState(int state){
  // Send ultrasonic state (6 if obstacle, 5 if free) to high level system
  Serial.write(byte(state));
}
  
