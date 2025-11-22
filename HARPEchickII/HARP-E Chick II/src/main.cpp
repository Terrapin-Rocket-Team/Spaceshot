#include <Arduino.h>
#include "MS5611.h"
#include <SPI.h>
#include <SD.h>   //SdFat SD;
#include <Wire.h> //Needed for I2C to GNSS

#include <SparkFun_u-blox_GNSS_v3.h> //http://librarymanager/All#SparkFun_u-blox_GNSS_v3

MS5611 MS5611(0x77);

// include pins
#define DROGUE_PIN 5
#define MAIN_PIN 6
#define BUZZER_PIN 7

// STAGING
#define stage_GROUND 1
#define stage_RISING 2
#define stage_FALLING 3
#define stage_LANDED 4

// BAROMETER GLOBAL VARS
float curPressure = 0.0;
float BasePressure = 0.0;
float startingAlt = 0.0;
float maxAltitude = 0.0;
float curAltitude;
float lastAlt;
float deltaAlt;
int stage = stage_GROUND;
float velocity;
float lastVelocity;
float acceleration;
int delayval;

unsigned long apogeeTime = 0;
float apogeeAlt = 0.0;

bool drogueDeployed = false;
bool mainDeployed = false;

const float LIFTOFF_DELTA_ALT = 50.0;
const float LANDING_WINDOW = 100.0;
const float LANDING_DELTA_ALT = 1.0;

const float DROGUE_ALTITUDE_AGL = 600.0; // arbitrary values
const float MAIN_ALTITUDE_AGL = 100.0;

SFE_UBLOX_GNSS myGNSS;
int fileWork = 0;

// GPS & buzzer stuff
long lastTime = 0; //Tracks the passing of 2000ms (2 seconds)
const byte buzzer = 7;
long first_alt = 0;
byte fix_type;
byte number = 0;


void printPVTdata(UBX_NAV_PVT_data_t *ubxDataStruct) {
  File myFile = SD.open("test1.txt", FILE_WRITE);

  Serial.println();
  myFile.println();


  Serial.print(F("Time: "));         // Print the time
  myFile.print(F("Time: "));         // Print the time

  uint8_t hms = ubxDataStruct->hour; // Print the hours
  if (hms < 10)
  {
    Serial.print(F("0")); // Print a leading zero if required
    myFile.print(F("0"));
  }
  Serial.print(hms);
  Serial.print(F(":"));
  myFile.print(hms);
  myFile.print(F(":"));
  hms = ubxDataStruct->min; // Print the minutes
  if (hms < 10)
  {
    Serial.print(F("0")); // Print a leading zero if required
    myFile.print(F("0"));
  }
  myFile.print(hms);
  myFile.print(F(":"));
  hms = ubxDataStruct->sec; // Print the seconds
  if (hms < 10)
  {
    Serial.print(F("0")); // Print a leading zero if required
    myFile.print(F("0"));
  }
  Serial.print(hms);
  Serial.print(F("."));
  myFile.print(hms);
  myFile.print(F("."));
  uint32_t millisecs = ubxDataStruct->iTOW % 1000; // Print the milliseconds
  if (millisecs < 100)
  {
    Serial.print(F("0"));
    myFile.print(F("0"));
  } // Print the trailing zeros correctly
  if (millisecs < 10)
  {
    Serial.print(F("0"));
    myFile.print(F("0"));
  }
  Serial.print(millisecs);
  myFile.print(millisecs);

  int32_t latitude = ubxDataStruct->lat; // Print the latitude
  Serial.print(F(" Lat: "));
  Serial.print(1.0 * latitude / 10000000, 7);
  myFile.print(F(" Lat: "));
  myFile.print(1.0 * latitude / 10000000, 7);

  int32_t longitude = ubxDataStruct->lon; // Print the longitude
  Serial.print(F(" Long: "));
  Serial.print(1.0 * longitude / 10000000, 7);
  myFile.print(F(" Long: "));
  myFile.print(1.0 * longitude / 10000000, 7);

  int32_t altitude = ubxDataStruct->hMSL; // Print the height above mean sea level
  Serial.print(F(" Height above MSL: "));
  Serial.print(altitude * 0.001);
  Serial.println(F(" (m)"));
  myFile.print(F(" Height above MSL: "));
  myFile.print(altitude * 0.001);
  myFile.println(F(" (m)"));
  // c write to file
  // fprintf(fptr, "Time: ");
  // //if (hms < 10) fprintf(fptr,"0"); // Print a leading zero if required
  // fprintf(fptr,"%02d:%02d:%02d.%04lu",ubxDataStruct->hour, ubxDataStruct->min, ubxDataStruct->sec, ubxDataStruct->iTOW % 1000);
  // fprintf(fptr, " Lat: %02.0000000f Long: %02.0000000f", 1.0*latitude/10000000, 1.0*longitude/10000000);
  // fprintf(fptr," Height above MSL: %f (m)", altitude*0.001);
  // fclose(fptr);
}
void logData() {}

void setup() {
  // Begin Serial, wire and SD card
  Serial.begin(115200);
  delay(1000);
  Wire.begin(); // Start I2C
  File myFile = SD.open("test1.txt", FILE_WRITE);

  // set other pins
  pinMode(DROGUE_PIN, OUTPUT);
  pinMode(MAIN_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(DROGUE_PIN, LOW);
  digitalWrite(MAIN_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // Start MS5611 and GPS
  while (!MS5611.begin()) {
    Serial.println("MS5611 not found, check wiring!");
    delay(1000);
  }
  // Buzz to indicate barometer started
  digitalWrite(BUZZER_PIN, HIGH);
  delay(200);
  digitalWrite(BUZZER_PIN, LOW);
  delay(200);
  digitalWrite(BUZZER_PIN, HIGH);
  delay(200);
  digitalWrite(BUZZER_PIN, LOW);
  delay(200);
  while (myGNSS.begin() == false) { // Connect to the u-blox module using Wire port
    Serial.println(F("u-blox GNSS not detected at default I2C address. Retrying..."));
    delay(1000);
  }
  // buzzer tone to indicate GPS connected
  tone(buzzer, 1000, 3000);    // Sounds buzzer for 3 seconds if GPS is connected
  Serial.println("GPS connected");
  delay(4500);
  fix_type = myGNSS.getFixType();
  if (fix_type > 3){
    tone(buzzer, 1000, 2000);               //checks if GPS has lock on satellites
    Serial.println("Lock on satellites");
  }

  // Barometer get first values
  Serial.println("MS5611 Found");
  MS5611.read();
  startingAlt = MS5611.getAltitude(MS5611.getPressure());

  // Set up GPS
  myGNSS.setI2COutput(COM_TYPE_UBX); // Set the I2C port to output UBX only (turn off NMEA noise)
  myGNSS.setNavigationFrequency(2); // Produce two solutions per second
  myGNSS.setAutoPVTcallbackPtr(&printPVTdata); // Enable automatic NAV PVT messages with callback to printPVTdata

  // Calibrating base altitude
  float sumAlt = 0.0;
  const int samples = 20;
  for (int i = 0; i < samples; i++) {
    MS5611.read();
    sumAlt += MS5611.getAltitude(MS5611.getPressure());
    delay(50);
  }

  startingAlt = sumAlt / samples;
  curAltitude = startingAlt;
  lastAlt = startingAlt;
  maxAltitude = startingAlt;

  Serial.print("Starting altitude: ");
  Serial.println(startingAlt);
  myFile.print("Starting altitude: ");
  myFile.println(startingAlt);
}

void loop() {
  File myFile = SD.open("test1.txt", FILE_WRITE);

  // start writing to microSD (currently writing to serial)
  lastAlt = curAltitude;
  lastVelocity=velocity;
  MS5611.read();
  curAltitude = MS5611.getAltitude(MS5611.getPressure());
  deltaAlt = lastAlt - curAltitude;
  velocity=1000.0*deltaAlt/(1.0*delayval);
  acceleration=1000.0*(velocity-lastVelocity)/(1.0*delayval);

  float altitudeAGL = curAltitude - startingAlt;
  // GPS
  myGNSS.checkUblox(); // Check for the arrival of new data and process it.
  myGNSS.checkCallbacks(); // Check if any callbacks are waiting to be processed.
  long GPSaltitude = myGNSS.getAltitudeMSL();

  // Ground
  if (stage == stage_GROUND) {
    delayval=2000;
    // Check whether altitude has risen above liftoff cut off (currently set to 50)
    if (altitudeAGL - LIFTOFF_DELTA_ALT > 0) {
      stage = stage_RISING;
      myFile.print("Now lifting off!");
    }
    if (first_alt==0) first_alt=GPSaltitude;
    delay(delayval);
  }
  // Rising
  if (stage == stage_RISING) {
    delayval=1000;
    // update max altitude
    if (maxAltitude < curAltitude) maxAltitude = curAltitude;

    // check if at top or if switched to falling
    // track velocity, deltaAlt will be smaller when it gets closer to apogee and then begins to fall
    // if deltaAlt is positive, make stage now falling -- calc acceleraction - if acceleration is around g is now falling
    if (deltaAlt > 1) {
      stage = stage_APOGEE;
      apogeeTime = millis();
      apogeeAlt = curAltitude;
      maxAltitude = curAltitude;
    }
    delay(delayval);
  }
  // Apogee
  if (stage == stage_APOGEE) {
    delayval=500;
    // update max altitude
    if (maxAltitude < curAltitude) maxAltitude = curAltitude;
    // check if falling at >1m/s
    if (velocity > 1) {
      stage = stage_FALLING;
    }
    delay(delayval);
  }
  // Falling
  if (stage == stage_FALLING) {
    delayval=500;
    unsigned long timeSinceApogeeMs = millis() - apogeeTime;
    float timeSinceApogeeSec = timeSinceApogeeMs / 1000.0;

    if (!drogueDeployed && timeSinceApogeeSec > 1.0) {
      drogueDeployed = true;
      digitalWrite(DROGUE_PIN, HIGH);
    }

    if (!mainDeployed && altitudeAGL < MAIN_ALTITUDE_AGL) {
      mainDeployed = true;
      digitalWrite(MAIN_PIN, HIGH);
    }

    // check if landed
    if (fabs(deltaAlt) < LANDING_DELTA_ALT && fabs(altitudeAGL) < LANDING_WINDOW) {
      stage = stage_LANDED;
    }
    delay(delayval);
  }
  // Landed
  if (stage == stage_LANDED) {
    delayval=5000;
    // digitalWrite(BUZZER_PIN, HIGH);
    // delay(200);
    // digitalWrite(BUZZER_PIN, LOW);
    // delay(800);
    delay(delayval);
  }
}
