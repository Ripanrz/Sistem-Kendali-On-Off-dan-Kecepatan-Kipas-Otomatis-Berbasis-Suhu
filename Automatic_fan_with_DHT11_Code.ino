#include "DHT.h"

#define DHTPIN A0       // Pin data DHT11 terhubung ke pin A0
#define DHTTYPE DHT11   // Menggunakan DHT11
DHT dht(DHTPIN, DHTTYPE);

float tempInCelcius;
int fan = 9;
unsigned long time_send;
unsigned long prev_time_send;
bool systemActive = false; // Status apakah sistem hidup atau mati
char receivedChar;         // Variabel untuk menerima karakter dari GUI

void setup()
{
  Serial.begin(9600);     // Inisialisasi komunikasi serial
  pinMode(fan, OUTPUT);   // Pin kipas sebagai OUTPUT
  dht.begin();            // Memulai sensor DHT11
}

void loop()
{
  // Membaca data serial dari GUI
  if (Serial.available() > 0)
  {
    receivedChar = Serial.read(); // Membaca karakter tunggal dari GUI
    if (receivedChar == '1')
    {
      systemActive = true; // Hidupkan sistem
    }
    else if (receivedChar == '0')
    {
      systemActive = false; // Matikan sistem
      analogWrite(fan, 0); // Memastikan kipas mati saat sistem dimatikan
    }
  }

  if (systemActive) // Jika sistem dihidupkan
  {
    time_send = millis() - prev_time_send;
    if (time_send > 500) // Perbarui setiap 500ms
    {
      tempInCelcius = dht.readTemperature();
      
      if (tempInCelcius < 25)
      {
        analogWrite(fan, 0); // Kipas mati
        Serial.print("ON");
        Serial.print(":");
        Serial.println(tempInCelcius);
      }
      else if (tempInCelcius >= 25 && tempInCelcius <= 30)
      {
        analogWrite(fan, 102); // Kecepatan rendah
        Serial.print("ON");
        Serial.print(":");
        Serial.println(tempInCelcius);
      }
      else if (tempInCelcius > 30 && tempInCelcius <= 35)
      {
        analogWrite(fan, 153); // Kecepatan sedang
        Serial.print("ON");
        Serial.print(":");
        Serial.println(tempInCelcius);
      }
      else if (tempInCelcius > 35)
      {
        analogWrite(fan, 255); // Kecepatan maksimum
        Serial.print("ON");
        Serial.print(":");
        Serial.println(tempInCelcius);
      }
      prev_time_send = millis();
    }
  }
  else // Jika sistem dimatikan
  {
    analogWrite(fan, 0); // Pastikan kipas mati
    time_send = millis() - prev_time_send;
    if (time_send > 500)
    {
      Serial.print("OFF");
      Serial.print(":");
      Serial.println("0");
      prev_time_send = millis();
    }
  }
}
