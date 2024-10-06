#include <Servo.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal_I2C.h>

byte SongID = 4;
#define CMD_SET_VOLUME 0X06//0*06           פקודה להגדרת עוצמת שמע    
#define CMD_SEL_DEV 0X09//בחירת התקן
#define DEV_TF 0X02//התקן מסוג SD  
#define CMD_PLAY_FOLDER_FILE 0X0F//נגן את הקובץ בתיקיה
#define ARDUINO_RX 4//should connect to TX of the Serial MP3 Player module
#define ARDUINO_TX 2 //connect to RX of the module


Servo myservo;  // create servo object to control a servo
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // Set the LCD I2C address
SoftwareSerial MP3(ARDUINO_RX, ARDUINO_TX);//ראשון RX

bool catOutside = false;
bool flag = true;
bool isCat = false;
const int fileLength = 3000;// זמן למנגינה
byte folder = 1;// שם התיקיה 01 שם השיר 001
const byte POTO = A0;
int positionVal = 0;
int doorOpenDelay=5000;
char inChar='0';
void setup() {
  Serial.begin(9600);
  myservo.attach(12);  // attaches the servo on pin 12 to the servo object
  lcd.begin(16, 2); // set up the LCD's number of columns and rows:חייבים להגדיר
  lcd.setCursor(0, 0);//התחלת כתיבה בשורה שניה מקום אפס
  lcd.clear();
  
  MP3.begin(9600);//איתחול תקשורת טורית   לפי הגדרת סופטוורסריאל
  delay(500);//Wait chip initialization is complete
  sendCommand(CMD_SEL_DEV, DEV_TF);//select TF/SD card
  delay(200);
  sendCommand(CMD_SET_VOLUME, 20);//set volume 0-30
  
  
}

void loop() {

  positionVal = analogRead(POTO);

  if(Serial.available()){
    inChar=Serial.read();
  }

  /********************screen************************/
  if (catOutside && !flag) {
    lcd.clear();
    lcd.print("cat outside");
    flag = true;
  }
  if (!catOutside && flag) {
    lcd.clear();
    lcd.print("cat inside");
    flag = false;
  }

  /**********open door when cat is inside***********/
  positionVal = analogRead(POTO);
  if (positionVal >500 && !catOutside) {
    
    playSong(01, 002);
    delay(fileLength);
    myservo.write(180);     // open door
    delay(doorOpenDelay);
    myservo.write(90);   //close door
    catOutside = true;
  }


  /**********open door when cat is outside***********/
  if (catOutside && inChar == '2') { //computer will send via serial communication
    Serial.println("");
    playSong(01, 001);
    delay(fileLength);
    myservo.write(180);     // open door
    delay(doorOpenDelay);
    myservo.write(90);   //close door    
    catOutside = false;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
  }

}

  //חייבים
  void playSong(byte folder, byte song) {
  sendCommand(CMD_PLAY_FOLDER_FILE, folder, song);
  }

  void sendCommand(byte command, unsigned int dat) {
  static byte Send_buf[8] = {0} ;
  delay(20);
  Send_buf[0] = 0x7e; //starting byte
  Send_buf[1] = 0xff; //version
  Send_buf[2] = 0x06; //the number of bytes of the command without starting byte and ending byte
  Send_buf[3] = command; //
  Send_buf[4] = 0x00;//0x00 = no feedback, 0x01 = feedback
  Send_buf[5] = (byte)(dat >> 8);//datah
  Send_buf[6] = (byte)(dat); //datal
  Send_buf[7] = 0xef; //ending byte
  for (byte i = 0; i < 8; i++) {
    MP3.write(Send_buf[i]) ;
  }
  }

  //חייבים
  void sendCommand(byte command, byte datH, byte datL)
  {
  static byte Send_buf[8] = {0} ;
  delay(20);
  Send_buf[0] = 0x7e; //starting byte
  Send_buf[1] = 0xff; //version
  Send_buf[2] = 0x06; //the number of bytes of the command without starting byte and ending byte
  Send_buf[3] = command; //
  Send_buf[4] = 0x00;//0x00 = no feedback, 0x01 = feedback
  Send_buf[5] = datH;//datah
  Send_buf[6] = datL; //datal
  Send_buf[7] = 0xef; //ending byte
  for (byte i = 0; i < 8; i++) {
    MP3.write(Send_buf[i]) ;
  }
  }