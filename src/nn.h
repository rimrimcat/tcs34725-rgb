#ifndef NN_H
#define NN_H

#include <Arduino.h>

void forward(float inputs[3], float outputs[3]);
void post_process(float outputs[3]);
void predict(float inputs[3], float outputs[3]);

#endif // NN_H