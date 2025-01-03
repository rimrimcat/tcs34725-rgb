# tcs34725-rgb

My first arduino project on making the TCS34725 RGB color sensor output more accurate RGB values. This repository contains three folders: src, scripts, and data. Prediction can be done by directly by uploading main.cpp directly.

## Data collection

Data was collected from sensor facing the monitor screen. Raw sensor values (R,G,B) were divided by the integration time and multiplied by a factor (1000). Such formulation allows to take into account the absolute brightness, in contrast to when normalizing by the CLEAR value, which only gives the relative brightness. The file scripts/collect_data.py can be edited to record the values into data/test.csv.

## Model fitting

Lasso model was used fit the parameters (refer to scripts/calibrate_linear.py). The obtained R^2 score was 0.9887 and the mean squared error was 79.4348. The model works good, but is not perfect; it may output values less than 0 and above 255. In the implementation, the prediction values were clipped to be within [0, 255].