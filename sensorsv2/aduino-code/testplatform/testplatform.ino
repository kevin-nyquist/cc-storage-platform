#include <SoftwareSerial.h>

// for gikfun DS18B20 tm1 sensor
#include <OneWire.h>
#include <DallasTemperature.h>

//air co2 temo hum
#include <SensirionI2CScd4x.h>
#include <Wire.h>
SensirionI2CScd4x scd4x;

// for ec1 Gravity analog ec
#include "DFRobot_EC10.h"
#include <EEPROM.h>
DFRobot_EC10 ec;

float def_temperature = 25.00;


//for moi2
const int dry = 465; // value for dry sensor
const int wet = 191; // value for wet sensor

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readString();

    if (command == "start") {
      Serial.println("sensing starting...");
     //test();
      tm1(6);
      ph1(2,3);
      ph2(A4);
      ec1(4,5);
      ec2(A2);
      moi2(A3);
      orp1(A5);
      orp2(A0,A1);
      airtmhm();
      delay(500);
      Serial.println("EOF");
    }
  }
}


void ph1(int rx, int tx){
  SoftwareSerial phserial(rx, tx);
  phserial.begin(9600);
  phserial.print('\r');
  String sensorstring = "";
  int i=0;
  while(true){
    if (phserial.available() > 0){
      char inchar = (char)phserial.read();            
      sensorstring += inchar;                           
      if (inchar == '\r'){
        i++;
        Serial.println("sensorid: ph1,phValue: "+sensorstring);
        // if (isNumberOrFloat(sensorstring)) {
        //    Serial.println("sensorid: ph1,phValue: "+sensorstring);
        // }
       
        sensorstring="";                 
      }
      if(i>10){
        break;
      }
    }
  }
}

void ph2(int analogpin){
  float ph4v = 1.6031; // calibrations
  float ph10v = 2.2043;
  float calibrationOffset = -0.0065;
  for (int i = 0; i < 10; i++) {
    // Read the analog value from the sensor
    int analogvalue = analogRead(analogpin);
    float voltage = (analogvalue / 1023.0) * 5.0;
    float pH = 10 - ((ph10v - voltage) / (ph10v - ph4v) * 6) + calibrationOffset;
    Serial.println("sensorid: ph2,ori: "+String(analogvalue) +",phValue: "+String(pH));
    delay(500);
  }

  // float avg = getAverageOfLargest5(analogpin, 10);
  // float voltage = (avg / 1023.0) * 5.0;
  // Serial.println("average voltage "+String(voltage,4));
  // float pH = 10 - ((ph10v - voltage) / (ph10v - ph4v) * 6) + calibrationOffset;
  // Serial.println("ph value is "+String(pH,4));
}


void ec1(int rx, int tx){
  SoftwareSerial ec1serial(rx, tx);
  ec1serial.begin(9600);
  ec1serial.print('\r');
  String sensorstring = "";
  int i=0;
  while(true){
    if (ec1serial.available() > 0){
      char inchar = (char)ec1serial.read();            
      sensorstring += inchar;                           
      if (inchar == '\r'){
        i++;
        char sensorstring_array[30];
        char *EC;
        sensorstring.toCharArray(sensorstring_array, 30);
        EC = strtok(sensorstring_array, ",");

        Serial.println("sensorid: ec1,ecValue: "+String(EC));
        sensorstring="";                 
      }
      if(i>10){
        break;
      }
    }
  }
}

void ec2(int apin){
  ec.begin();
  for(int i=0;i<10;i++){
    readec2(apin);
    delay(500);
  }
}
void readec2(int anpin){
  float voltage = analogRead(anpin)/1024.0*5000;  // read the voltage
  Serial.print("sensorid: ec2,voltage: ");
  Serial.print(voltage);
  float temperature = readTemperature();  // read your temperature sensor to execute temperature compensation
  float ecValue =  ec.readEC(voltage,temperature);  // convert voltage to EC with temperature compensation
  Serial.print(",temperature: ");
  Serial.print(temperature,2);
  Serial.print("^C,EC: ");
  Serial.print(ecValue,2);
  Serial.println("ms/cm");

}

void tm1(int bus){
  OneWire oneWire(bus);
  DallasTemperature sensors(&oneWire);
  sensors.begin();
  for(int i=0;i<10;i++){
    sensors.requestTemperatures();
    float tempC = sensors.getTempCByIndex(0);
    // Check if reading was successful
    if (tempC != DEVICE_DISCONNECTED_C){
      Serial.println("sensorid: tm1,temp: "+String(tempC));
    }
    else{
      Serial.println("Error: Could not read temperature data");
    }
  }
} 

void airtmhm(){
  Wire.begin();
  scd4x.begin(Wire);
  uint16_t error;
  error = scd4x.stopPeriodicMeasurement();
  if (error) {
     Serial.println("sensorid: airtmhm,ori: error");
     return;
  }
  error = scd4x.startPeriodicMeasurement();
  if (error) {
      Serial.println("sensorid: airtmhm,ori: error");
      return;
  }

  delay(100);

  // Read Measurement
   Serial.println("sensorid: airtmhm,ori: started");
  for(int i=0;i<2;i++){
    uint16_t co2 = 0;
    float temperature = 0.0f;
    float humidity = 0.0f;
    bool isDataReady = false;
    error = scd4x.getDataReadyFlag(isDataReady);
    if (error) {
        Serial.println("sensorid: airtmhm,ori: error");
        return;
    }
    unsigned long startTime = millis();
    while (millis() - startTime < 10000) { // Timeout after 10 seconds
      if (isDataReady) {
        error = scd4x.readMeasurement(co2, temperature, humidity);
        if (error) {
          Serial.println("sensorid: airtmhm,ori: error");
          return;
        }else {
          Serial.println("sensorid: airtmhm,co2: "+String(co2)+",temp: "+String(temperature)+",humidity: "+String(humidity));
        }
        break;
      }
      delay(10);
    } 
  }
}

float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
  OneWire oneWire(6);
  DallasTemperature sensors(&oneWire);
  sensors.begin();
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  // Check if reading was successful
  if (tempC != DEVICE_DISCONNECTED_C){
    return tempC;
  }
  else{
    return def_temperature;
  }
}

void moi2(int anpin){

  for(int i=0;i<10;i++){
    int sensorVal = analogRead(anpin);
    //Serial.println("sensor value: "+String(sensorVal));
    int percentageHumididy = map(sensorVal, wet, dry, 100, 0);
    if (percentageHumididy < 0){
      percentageHumididy =0;
    }
    Serial.println("sensorid: moi2,ori: "+String(sensorVal)+",moiValue: " + String(percentageHumididy)+"%");
    delay(100);
  }
}

void orp1(int anpin){
  float intercept = -559.793;
  float slope = 466.875;

  for(int i=0;i<10;i++){
    int sensorVal = analogRead(anpin);
    float voltage = (sensorVal / 1023.0) * 5.0;
    float orpReading= intercept + voltage * slope;
    Serial.println("sensorid: orp1,ori: "+String(sensorVal)+",orpValue: " + String(orpReading));
    // Serial.println("Vol value: " + String(voltage));
    // Serial.println("ORP value: " + String(orpReading));
    delay(100);
  }
}

void orp2(int orppin,int calpin){
  float VOLTAGE = 5.00;   //vcc voltage(unit: V)
  int LED = 13;        //operating instructions
  int ArrayLenth = 10; //times of collection
  
  double orpValue; 
  // double offset=0.0;
  int offset=0;
  bool is_calibrated = false;
  int wait_count = 5;
  int orpArray[ArrayLenth];
  int orpArrayIndex=0;
  double avergearray(int* arr, int number);
  pinMode(LED,OUTPUT);
  pinMode(calpin,OUTPUT);
  // digitalWrite(calpin, LOW);
  digitalWrite(calpin, HIGH);

  unsigned long orpTimer=millis();   //analog sampling interval
  unsigned long printTime=millis();
  int i=0;
  while(true){

    if(millis() >= orpTimer)
    {
      orpTimer=millis()+20;
      orpArray[orpArrayIndex++]=analogRead(orppin);    //read an analog value every 20ms
      if (orpArrayIndex==ArrayLenth) {
        orpArrayIndex=0;
      }   
      orpValue=((30*(double)VOLTAGE*1000)-(75*avergearray(orpArray, ArrayLenth)*VOLTAGE*1000/1024))/75-offset;
    }
    if(millis() >= printTime)   //Every 800 milliseconds, print a numerical
    {
      
      if(!is_calibrated) {
        if(wait_count==0){
          offset += (int)orpValue; 
          is_calibrated = true;
          digitalWrite(calpin, LOW);
          Serial.println("offset: "+ String(offset)+"mV");
        }
        wait_count--;
      }
      else {
        Serial.println("sensorid: orp2, orpValue: "+String(orpValue)+"mV");
        i++;
        digitalWrite(LED,1-digitalRead(LED)); // convert the state of the LED indicator      
      } 
      printTime=millis()+800;   
      if(i>=10){
        break;
      }
    }
    
  }


}

void test(){
  Serial.println("hey");
  for (int i = 0; i <= 5; i++) {
    delay(1000);
    Serial.println(i);
  }
}

float getAverageOfLargest5(int analogPin, int numReadings) {
  int readings[numReadings];       // Array to store readings

  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;             // Initialize the array
  }
  for (int i = 0; i < numReadings; i++) {
    // Read the analog value from the sensor
    int analogvalue = analogRead(analogPin);
    Serial.println("analog value  "+String(analogvalue));
    readings[i] = analogvalue;
    delay(1000);
  }
  bubbleSort(readings,10);
  float total=0.0;
  for(int i =5;i<numReadings;i++){
    total+=readings[i];
  }
  float avg = total/5;
  return avg;
}

void bubbleSort(int arr[], int size) {
  for (int i = 0; i < size - 1; i++) {
    for (int j = 0; j < size - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        // Swap arr[j] and arr[j+1]
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
    }
  }
}

bool isNumberOrFloat(String str) {
  bool hasDecimal = false;
  for (size_t i = 0; i < str.length(); i++) {
    if (str.charAt(i) == '.') {
      if (hasDecimal) {
        return false; // More than one decimal point
      }
      hasDecimal = true;
    } else if (!isDigit(str.charAt(i))) {
      return false; // Non-digit character
    }
  }
  return str.length() > 0; // At least one character
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    printf("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
return avg;
}

