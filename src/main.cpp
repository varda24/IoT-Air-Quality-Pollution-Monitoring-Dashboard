#include <Arduino.h>
#include <DHTesp.h>

#define DHT_PIN 15
#define MQ135_PIN 34

#define GREEN_LED 18
#define YELLOW_LED 19
#define RED_LED 21
#define BUZZER 23

DHTesp dht;

String getAQIStatus(int aqi) {
  if (aqi <= 50)
    return "GOOD";
  else if (aqi <= 100)
    return "MODERATE";
  else if (aqi <= 200)
    return "POOR";
  else
    return "HAZARDOUS";
}

void setup() {

  Serial.begin(115200);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  dht.setup(DHT_PIN, DHTesp::DHT22);

  Serial.println("\n=================================");
  Serial.println("AIR QUALITY MONITORING SYSTEM");
  Serial.println("=================================");
}

void loop() {

  TempAndHumidity data = dht.getTempAndHumidity();

  // Simulated MQ135 value from potentiometer
  int mqValue = analogRead(MQ135_PIN);

  // Convert sensor value to AQI range
  int aqi = map(mqValue, 0, 4095, 0, 500);

  String status = getAQIStatus(aqi);

  // Reset outputs
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);
  noTone(BUZZER);

  // Alert Logic
  if (status == "GOOD") {

    digitalWrite(GREEN_LED, HIGH);

  } else if (status == "MODERATE") {

    digitalWrite(YELLOW_LED, HIGH);

  } else if (status == "POOR") {

    digitalWrite(YELLOW_LED, HIGH);

  } else {

    digitalWrite(RED_LED, HIGH);
    tone(BUZZER, 1000);
  }

  // Serial Output
  Serial.println("\n----------------------------------");

  Serial.print("MQ135 Raw Value: ");
  Serial.println(mqValue);

  Serial.print("AQI Value: ");
  Serial.println(aqi);

  Serial.print("Temperature: ");
  Serial.print(data.temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(data.humidity);
  Serial.println(" %");

  Serial.print("Air Quality Status: ");
  Serial.println(status);

  if (status == "HAZARDOUS")
    Serial.println("ALERT: Dangerous Pollution Level!");
  else if (status == "POOR")
    Serial.println("ALERT: Poor Air Quality");
  else
    Serial.println("ALERT: Normal");

  delay(3000);
}