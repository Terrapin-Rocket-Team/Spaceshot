#include <Arduino.h>
#include "MS5611.h"
#include <SPI.h>
#include <SdFat.h>
#include <Wire.h>
#include <SparkFun_u-blox_GNSS_v3.h>

// Use SdFat for Teensy 4.1
SdFat SD;

// Hardware instances
MS5611 baro(0x77);
SFE_UBLOX_GNSS myGNSS;

// Pin definitions
#define BUZZER_PIN 37

// Flight stages
enum FlightStage
{
  STAGE_GROUND = 0,
  STAGE_ASCENT = 1,
  STAGE_DESCENT = 2,
  STAGE_MAIN = 3,
  STAGE_LANDED = 4
};

// Stage detection thresholds
#define LAUNCH_ALT_THRESHOLD 50.0   // meters (GPS)
#define DESCENT_TIME_THRESHOLD 5000 // milliseconds
#define MAIN_ALT_THRESHOLD 1000.0   // meters (GPS)
#define LANDED_TIME_THRESHOLD 10000 // milliseconds
#define LANDED_VEL_THRESHOLD 1.0    // m/s

// Logging intervals for each stage (milliseconds)
const unsigned long LOG_INTERVAL[5] = {
    2000, // GROUND: 2s
    500,  // ASCENT: 0.5s
    1000, // DESCENT: 1s
    2000, // MAIN: 2s
    2000  // LANDED: 2s
};

// Global state variables
FlightStage currentStage = STAGE_GROUND;
unsigned long lastLogTime = 0;
unsigned long descentStartTime = 0;
unsigned long landedStartTime = 0;
bool descentDetected = false;
bool landedDetected = false;

// Baseline altitudes (set on startup/first fix)
float baselineGPSAlt = 0.0;
float baselineBaroAlt = 0.0;
bool gpsBaselineSet = false;
bool baroBaselineSet = false;

// File handling
String dataFileName = "";
String eventFileName = "";
FsFile dataFile;
FsFile eventFile;

// Sensor initialization flags
bool baroInitialized = false;
bool gpsInitialized = false;
bool gpsHasFix = false;
bool gpsFixLogged = false;
bool gpsLostFixWarned = false;
bool gpsEverHadFix = false; // Track if GPS has ever had a valid fix
bool sdInitialized = false;
unsigned long gpsInitTime = 0; // Track when GPS was initialized
#define GPS_SETTLE_TIME 120000 // 2 minutes in milliseconds

// Data structure for logging
struct SensorData
{
  unsigned long timestamp;
  FlightStage stage;
  float baroAlt;
  float baroPres;
  float gpsAlt;
  float gpsLat;
  float gpsLon;
  float gpsVelZ;
  int gpsSatCount;
};

SensorData currentData;

// Function prototypes
void initBuzzer();
void initBarometer();
void initGPS();
void initSDCard();
void buzzPattern(int pattern);
String getNextFileName(String prefix, String extension);
void logEvent(String event);
void logSensorData();
void updateStage();
void readSensors();
const char *getStageString(FlightStage stage);

void setup()
{
  Serial.begin(115200);
  delay(1000);

  Serial.println(F("=== Flight Computer Initializing ==="));

  // Initialize buzzer first
  initBuzzer();

  // Initialize I2C
  Wire.begin();

  // Initialize SD card first so we can log everything
  initSDCard();

  // Create log files before sensor initialization
  dataFileName = getNextFileName("DATA", ".csv");
  eventFileName = getNextFileName("EVENT", ".txt");

  Serial.print(F("Data file: "));
  Serial.println(dataFileName);
  Serial.print(F("Event file: "));
  Serial.println(eventFileName);

  // Write CSV header
  dataFile = SD.open(dataFileName.c_str(), FILE_WRITE);
  if (dataFile)
  {
    dataFile.println(F("time_s,stage,baro_alt_m,baro_pres_pa,gps_alt_m,gps_lat_deg,gps_lon_deg,gps_vel_z_m_s,gps_sat_count"));
    dataFile.close();
  }

  // Write event log header
  logEvent("=== FLIGHT COMPUTER STARTUP ===");

  // Initialize barometer (will log its status)
  initBarometer();

  // Initialize GPS (will log its status)
  initGPS();

  // Log final initialization summary
  logEvent("=== INITIALIZATION COMPLETE ===");
  logEvent("SD Card: " + String(sdInitialized ? "OK" : "FAIL"));
  logEvent("Barometer: " + String(baroInitialized ? "OK" : "FAIL"));
  logEvent("GPS: " + String(gpsInitialized ? "OK" : "FAIL"));

  // Beep patterns: 1 beep = SD card, 2 beeps = baro, 3 beeps = GPS, 4 beeps = GPS fix (logged later)
  Serial.println(F("=== Initialization Complete ==="));

  // Beep for SD card
  if (sdInitialized)
  {
    Serial.println(F("Beeping 1x for SD card OK"));
    buzzPattern(1);
    delay(1000);
  }

  // Beep for barometer
  if (baroInitialized)
  {
    Serial.println(F("Beeping 2x for barometer OK"));
    buzzPattern(2);
    delay(1000);
  }

  // Beep for GPS
  if (gpsInitialized)
  {
    Serial.println(F("Beeping 3x for GPS OK"));
    buzzPattern(3);
    delay(1000);
  }

  lastLogTime = millis();
}

void loop()
{
  unsigned long currentTime = millis();

  // Read sensors
  readSensors();

  // Update flight stage
  updateStage();

  // Log data at appropriate interval for current stage
  if (currentTime - lastLogTime >= LOG_INTERVAL[currentStage])
  {
    logSensorData();
    lastLogTime = currentTime;
  }

  // Small delay to prevent overwhelming the system
  delay(10);
}

void initBuzzer()
{
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
  Serial.println(F("Buzzer initialized"));
}

void initBarometer()
{
  Serial.print(F("Initializing barometer..."));
  logEvent("Initializing barometer...");

  int attempts = 0;
  while (!baro.begin() && attempts < 5)
  {
    Serial.print(F("."));
    delay(500);
    attempts++;
  }

  if (attempts < 5)
  {
    baroInitialized = true;
    Serial.println(F(" OK"));
    logEvent("Barometer initialized successfully");

    // Calibrate barometer
    Serial.print(F("Calibrating barometer..."));
    delay(100);
    baro.read();
    Serial.println(F(" Done"));
    logEvent("Barometer calibration complete");
  }
  else
  {
    Serial.println(F(" FAILED"));
    logEvent("Barometer initialization FAILED after " + String(attempts) + " attempts");
  }
}

void initGPS()
{
  Serial.print(F("Initializing GPS..."));
  logEvent("Initializing GPS...");

  int attempts = 0;
  while (!myGNSS.begin() && attempts < 5)
  {
    Serial.print(F("."));
    delay(500);
    attempts++;
  }

  if (attempts < 5)
  {
    gpsInitialized = true;
    gpsInitTime = millis(); // Record initialization time
    Serial.println(F(" OK"));
    logEvent("GPS initialized successfully");

    // Configure GPS
    myGNSS.setI2COutput(COM_TYPE_UBX);
    myGNSS.setNavigationFrequency(2); // 2 Hz
    logEvent("GPS configured: 2 Hz update rate");

    Serial.println(F("GPS will acquire fix during normal operation (2 min settle time)"));
    logEvent("GPS searching for satellites... (2 min settle time before fix allowed)");
  }
  else
  {
    Serial.println(F(" FAILED"));
    logEvent("GPS initialization FAILED after " + String(attempts) + " attempts");
  }
}

void initSDCard()
{
  Serial.print(F("Initializing SD card..."));

  // Teensy 4.1 built-in SD card (SPI_SPEED is optional, SdioConfig is for SDIO mode)
  // For SdFat on Teensy 4.1, use SdioConfig
  if (SD.begin(SdioConfig(FIFO_SDIO)))
  {
    sdInitialized = true;
    Serial.println(F(" OK"));
  }
  else
  {
    Serial.println(F(" FAILED"));
  }
}

void buzzPattern(int count)
{
  // Beep 'count' times
  for (int i = 0; i < count; i++)
  {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(200);
  }
}

String getNextFileName(String prefix, String extension)
{
  if (!sdInitialized)
  {
    return prefix + "000" + extension;
  }

  int fileNumber = 0;
  String fileName;

  // Find next available file number
  do
  {
    fileName = prefix + String(fileNumber, DEC);
    while (fileName.length() < prefix.length() + 3)
    {
      fileName = prefix + "0" + fileName.substring(prefix.length());
    }
    fileName += extension;
    fileNumber++;
  } while (SD.exists(fileName.c_str()) && fileNumber < 1000);

  return fileName;
}

void logEvent(String event)
{
  unsigned long timestamp = millis();

  // Log to serial
  Serial.print(F("["));
  Serial.print(timestamp);
  Serial.print(F("] "));
  Serial.println(event);

  // Log to SD card
  if (sdInitialized)
  {
    eventFile = SD.open(eventFileName.c_str(), FILE_WRITE);
    if (eventFile)
    {
      eventFile.print(timestamp);
      eventFile.print(F(","));
      eventFile.println(event);
      eventFile.close();
    }
  }
}

void readSensors()
{
  currentData.timestamp = millis();
  currentData.stage = currentStage;

  // Read barometer
  if (baroInitialized)
  {
    baro.read();
    currentData.baroPres = baro.getPressure();

    // Get MSL altitude from pressure
    float baroMSL = baro.getAltitude();

    // Set baseline on first read
    if (!baroBaselineSet)
    {
      baselineBaroAlt = baroMSL;
      baroBaselineSet = true;
      logEvent("Barometer baseline set: " + String(baselineBaroAlt, 2) + " m MSL, " + String(currentData.baroPres, 2) + " hPa");
    }

    // Store as AGL (relative to baseline)
    currentData.baroAlt = baroMSL - baselineBaroAlt;
  }
  else
  {
    currentData.baroPres = 0.0;
    currentData.baroAlt = 0.0;
  }

  // Read GPS
  if (gpsInitialized)
  {
    myGNSS.checkUblox();
    myGNSS.checkCallbacks();

    // Check GPS fix status
    byte fixType = myGNSS.getFixType();
    bool currentlyHasFix = (fixType >= 3);

    // Get GPS data
    float gpsMSL = myGNSS.getAltitudeMSL() / 1000.0; // mm to m
    currentData.gpsLat = myGNSS.getLatitude() / 10000000.0;  // degrees
    currentData.gpsLon = myGNSS.getLongitude() / 10000000.0; // degrees

    // Get velocity from PVT data (NED down velocity in mm/s, negative means ascending)
    // We negate it so positive velocity means ascending
    int32_t velD = myGNSS.getNedDownVel();  // mm/s (positive = down)
    currentData.gpsVelZ = -(velD / 1000.0); // Convert to m/s and flip sign (positive = up)

    currentData.gpsSatCount = myGNSS.getSIV();

    // Set baseline if not set and we have good data
    if (!gpsBaselineSet && currentlyHasFix && gpsMSL > 0)
    {
      baselineGPSAlt = gpsMSL;
      gpsBaselineSet = true;
      logEvent("GPS baseline set: " + String(baselineGPSAlt, 2) + " m MSL");
    }

    // Store as AGL (relative to baseline)
    currentData.gpsAlt = gpsMSL - baselineGPSAlt;

    // Monitor GPS fix acquisition and loss
    // Only allow fix declaration after GPS_SETTLE_TIME has elapsed
    bool gpsSettled = (millis() - gpsInitTime) >= GPS_SETTLE_TIME;

    if (currentlyHasFix && !gpsHasFix && gpsSettled)
    {
      // Just acquired fix (after settle time)
      gpsHasFix = true;

      // Only beep and log the first time we ever get a fix
      // This avoids beeping if GPS starts with uninitialized data then immediately loses fix
      if (!gpsEverHadFix)
      {
        gpsEverHadFix = true;

        // Reset GPS baseline now that we have accurate data
        baselineGPSAlt = gpsMSL;
        gpsBaselineSet = true;
        logEvent("GPS baseline reset on fix: " + String(baselineGPSAlt, 2) + " m MSL");

        // Recalculate AGL with new baseline
        currentData.gpsAlt = gpsMSL - baselineGPSAlt;

        logEvent("GPS FIX ACQUIRED - Satellites: " + String(currentData.gpsSatCount) + ", Fix type: " + String(fixType));
        Serial.println(F("GPS fix acquired! Beeping 4x..."));
        buzzPattern(4);
        gpsFixLogged = true;
      }
      gpsLostFixWarned = false;
    }
    else if (!currentlyHasFix && gpsHasFix)
    {
      // Lost fix (only log if we've had a valid fix before)
      gpsHasFix = false;
      if (gpsEverHadFix)
      {
        logEvent("GPS FIX LOST - Satellites: " + String(currentData.gpsSatCount));
      }
      gpsLostFixWarned = false;
    }

    // Warn if no fix during flight
    if (!currentlyHasFix && currentStage != STAGE_GROUND && !gpsLostFixWarned)
    {
      Serial.println(F("WARNING: No GPS fix during flight!"));
      // Short warning beeps
      for (int i = 0; i < 3; i++)
      {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(100);
        digitalWrite(BUZZER_PIN, LOW);
        delay(100);
      }
      gpsLostFixWarned = true;
    }
  }
  else
  {
    currentData.gpsAlt = 0.0;
    currentData.gpsLat = 0.0;
    currentData.gpsLon = 0.0;
    currentData.gpsVelZ = 0.0;
    currentData.gpsSatCount = 0;
  }
}

void updateStage()
{
  FlightStage previousStage = currentStage;
  unsigned long currentTime = millis();

  // currentData.gpsAlt is already AGL (relative to baseline)
  float gpsAltAGL = currentData.gpsAlt;

  switch (currentStage)
  {
  case STAGE_GROUND:
    // Detect launch: GPS altitude > 50m AGL
    if (gpsBaselineSet && gpsAltAGL > LAUNCH_ALT_THRESHOLD)
    {
      currentStage = STAGE_ASCENT;
      logEvent("LAUNCH DETECTED - GPS Alt AGL: " + String(gpsAltAGL, 2) + " m, Baro Alt AGL: " + String(currentData.baroAlt, 2) + " m");
    }
    break;

  case STAGE_ASCENT:
    // Detect descent: GPS velocity Z < 0 for > 5 seconds
    if (currentData.gpsVelZ < 0)
    {
      if (!descentDetected)
      {
        descentDetected = true;
        descentStartTime = currentTime;
      }
      else if (currentTime - descentStartTime >= DESCENT_TIME_THRESHOLD)
      {
        currentStage = STAGE_DESCENT;
        logEvent("DESCENT DETECTED - Vel Z: " + String(currentData.gpsVelZ, 2) + " m/s, Alt AGL: " + String(gpsAltAGL, 2) + " m");
        descentDetected = false;
      }
    }
    else
    {
      descentDetected = false;
    }
    break;

  case STAGE_DESCENT:
    // Detect main deployment altitude: GPS alt < 1000m AGL
    if (gpsAltAGL < MAIN_ALT_THRESHOLD)
    {
      currentStage = STAGE_MAIN;
      logEvent("MAIN ALTITUDE REACHED - Alt AGL: " + String(gpsAltAGL, 2) + " m");
    }
    break;

  case STAGE_MAIN:
    // Detect landing: abs(velocity) < 1 m/s for > 10 seconds
    {
      float absVel = abs(currentData.gpsVelZ); // Absolute velocity

      if (absVel < LANDED_VEL_THRESHOLD)
      {
        if (!landedDetected)
        {
          landedDetected = true;
          landedStartTime = currentTime;
        }
        else if (currentTime - landedStartTime >= LANDED_TIME_THRESHOLD)
        {
          currentStage = STAGE_LANDED;
          logEvent("LANDED - Vel: " + String(absVel, 2) + " m/s, Alt AGL: " + String(gpsAltAGL, 2) + " m");
          landedDetected = false;
        }
      }
      else
      {
        landedDetected = false;
      }
      break;
    }

  case STAGE_LANDED:
    // Stay in landed state
    break;
  }

  // Log stage changes
  if (previousStage != currentStage)
  {
    logEvent("Stage changed: " + String(getStageString(previousStage)) + " -> " + String(getStageString(currentStage)));
  }
}

void logSensorData()
{
  // Convert timestamp from ms to seconds with 3 decimal points
  float timeSeconds = currentData.timestamp / 1000.0;

  // Build CSV line
  String dataLine = String(timeSeconds, 3) + ",";
  dataLine += String(currentData.stage) + ",";
  dataLine += String(currentData.baroAlt, 2) + ",";
  dataLine += String(currentData.baroPres, 2) + ",";
  dataLine += String(currentData.gpsAlt, 2) + ",";
  dataLine += String(currentData.gpsLat, 7) + ",";
  dataLine += String(currentData.gpsLon, 7) + ",";
  dataLine += String(currentData.gpsVelZ, 2) + ",";
  dataLine += String(currentData.gpsSatCount);

  // Output to Serial
  Serial.println(dataLine);

  // Output to SD card
  if (sdInitialized)
  {
    dataFile = SD.open(dataFileName.c_str(), FILE_WRITE);
    if (dataFile)
    {
      dataFile.println(dataLine);
      dataFile.close();
    }
  }
}

const char *getStageString(FlightStage stage)
{
  switch (stage)
  {
  case STAGE_GROUND:
    return "GROUND";
  case STAGE_ASCENT:
    return "ASCENT";
  case STAGE_DESCENT:
    return "DESCENT";
  case STAGE_MAIN:
    return "MAIN";
  case STAGE_LANDED:
    return "LANDED";
  default:
    return "UNKNOWN";
  }
}
