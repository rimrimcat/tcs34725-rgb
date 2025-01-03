#include "prints.h"

void print1(float a, String name = "", String extra = "")
{
    Serial.print(name);
    Serial.print(" ");
    Serial.print(a, 2);
    Serial.print(" ");
    Serial.print(extra);
    Serial.println(" ");
};

void print3(float r, float g, float b, String name = "", String extra = "")
{
    Serial.print(name);
    Serial.print(" (");
    Serial.print(r, 2);
    Serial.print(", ");
    Serial.print(g, 2);
    Serial.print(", ");
    Serial.print(b, 2);
    Serial.print(") ");
    Serial.print(extra);
    Serial.println(" ");
};

void print4(float r, float g, float b, float c, String name = "", String extra = "")
{
    Serial.print(name);
    Serial.print(" (");
    Serial.print(r, 2);
    Serial.print(", ");
    Serial.print(g, 2);
    Serial.print(", ");
    Serial.print(b, 2);
    Serial.print(", ");
    Serial.print(c, 2);
    Serial.print(") ");
    Serial.print(extra);
    Serial.println(" ");
};

