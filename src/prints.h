#ifndef PRINTS_H
#define PRINTS_H

#include <Arduino.h>

void print1(float a, String name = "", String extra = "");
void print3(float r, float g, float b, String name = "", String extra = "");
void print4(float r, float g, float b, float c, String name = "", String extra = "");

// Base case for the recursive variadic template
template <typename T>
void printn(T value)
{
    Serial.println(value);
};

// Recursive variadic template function
template <typename T, typename... Args>
void printn(T first, Args... rest)
{
    Serial.print(first);
    Serial.print(",");
    printn(rest...);
};

#endif // PRINTS_H