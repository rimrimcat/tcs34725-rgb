#include <nn.h>

const float COEFFS[3][6] = {
    {3.97060486, -1.47080107, -8.36473620e-1, -6.11288783e-3, 2.46096898e-3, 3.53639888e-3},
    {-1.39636026, 3.69652826, -1.01601590, 4.30188871e-3, -6.05889424e-3, 1.32184877e-3},
    {-6.50722096e-1, -1.22388610, 3.97931317, 1.32816576e-3, 1.63784209e-3, -5.38607976e-3}};

const float INTERCEPTS[3] = {-163.21512471, -72.10567674, -107.08278013};

void forward(float input[3], float output[3])
{
    const float input2[6] = {input[0], input[1], input[2], input[0] * input[0], input[1] * input[1], input[2] * input[2]};
    // For each output dimension
    for (int i = 0; i < 3; i++)
    {
        float sum = INTERCEPTS[i];

        // Dot product of input with coefficients
        for (int j = 0; j < 6; j++)
        {
            sum += COEFFS[i][j] * input2[j];
        }

        output[i] = sum;
    }
}

void post_process(float inputs[3])
{
    if (inputs[0] > 255)
    {
        inputs[0] = 255;
    }
    else if (inputs[0] < 0)
    {
        inputs[0] = 0;
    }

    if (inputs[1] > 255)
    {
        inputs[1] = 255;
    }
    else if (inputs[1] < 0)
    {
        inputs[1] = 0;
    }

    if (inputs[2] > 255)
    {
        inputs[2] = 255;
    }
    else if (inputs[2] < 0)
    {
        inputs[2] = 0;
    }
}

void predict(float inputs[3], float outputs[3])
{
    forward(inputs, outputs);
    post_process(outputs);
}