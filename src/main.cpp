#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include "Adafruit_TCS34725.h"

#include <prints.h>
#include <nn.h>

//
const int integ_time = TCS34725_INTEGRATIONTIME_300MS;
Adafruit_TCS34725 tcs = Adafruit_TCS34725(integ_time, TCS34725_GAIN_1X);
const int precision = 0;

unsigned long prev_millis;

// put function declarations here:
void getOutput(void)
{
  uint16_t r_raw, g_raw, b_raw, c_raw, colorTemp, lux;
  float r_t, g_t, b_t, c_t;
  unsigned long timestamp, time_diff;

  tcs.getRawData(&r_raw, &g_raw, &b_raw, &c_raw);
  colorTemp = tcs.calculateColorTemperature_dn40(r_raw, g_raw, b_raw, c_raw);
  lux = tcs.calculateLux(r_raw, g_raw, b_raw);

  timestamp = millis();
  time_diff = timestamp - prev_millis;

  r_t = (float)r_raw / time_diff * 1000;
  g_t = (float)g_raw / time_diff * 1000;
  b_t = (float)b_raw / time_diff * 1000;
  //c_t = (float)c_raw / time_diff * 1000;
  //r_t = (float)r_raw * 255 / c_raw;
  //g_t = (float)g_raw * 255 / c_raw;
  //b_t = (float)b_raw * 255 / c_raw;
  c_t = (float)log((double)c_raw / time_diff * 1000);

  // CSV FORMAT
  // timestamp, time_diff, r,   g,   b,   c,   colortemp, lux
  // printn(timestamp, time_diff, r_t, g_t, b_t, c_t, colorTemp, lux);
  printn(r_t, g_t, b_t, c_t);

  prev_millis = millis();
};

void testPredict(void)
{
  uint16_t r_raw, g_raw, b_raw, c_raw;
  float r_t, g_t, b_t, c_t;
  float outputs[3];

  unsigned long timestamp, time_diff;

  tcs.getRawData(&r_raw, &g_raw, &b_raw, &c_raw);

  timestamp = millis();
  time_diff = timestamp - prev_millis;

  r_t = (float)r_raw / time_diff * 1000;
  g_t = (float)g_raw / time_diff * 1000;
  b_t = (float)b_raw / time_diff * 1000;
  c_t = (float)c_raw / time_diff * 1000;

  float inputs[3] = {r_t, g_t, b_t};
  predict(inputs, outputs);

  // printn(r_t, g_t, b_t);
  printn(outputs[0], outputs[1], outputs[2]);

  prev_millis = millis();
};

void setup()
{
  Serial.begin(9600);

  if (tcs.begin())
  {
    // Serial.println("Found sensor");
    // printn("timestamp,integ_time,time_diff,r,g,b,c,colortemp,lux");
  }
  else
  {
    Serial.println("No TCS34725 found ... check your connections");
    while (1)
      ;
  }

  // Now we're ready to get readings!
}

void loop()
{
  // tcs.setInterrupt(true); // turn off LED
  //getOutput();
  testPredict();
}
