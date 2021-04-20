/*
  c
  - released
  b
  - Use FIR filters with fast_fft option

  The audio board uses the following pins.
  6 - MEMCS
  7 - MOSI
  9 - BCLK
  10 - SDCS
  11 - MCLK
  12 - MISO
  13 - RX
  14 - SCLK
  15 - VOL
  18 - SDA
  19 - SCL
  22 - TX
  23 - LRCLK
*/

#include <Audio.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>
#include <SerialFlash.h>
#include "filter.h"


#define LED 13



AudioInputI2S         audioInput;         // audio shield: mic or line-in
AudioFilterFIR        myFilterL;
AudioFilterFIR        myFilterR;
AudioOutputI2S        audioOutput;        // audio shield: headphones & line-out

// Create Audio connections between the components
// Route audio into the left and right filters
AudioConnection c1(audioInput, 0, myFilterL, 0);
AudioConnection c2(audioInput, 1, myFilterR, 0);
// Route the output of the filters to their respective channels
AudioConnection c3(myFilterL, 0, audioOutput, 0);
AudioConnection c4(myFilterR, 0, audioOutput, 1);
AudioControlSGTL5000 audioShield;

struct fir_filter {
  short *coeffs;
  short num_coeffs;    // num_coeffs must be an even number, 4 or higher
};

int num_coeff = 0;
int16_t filt[100000] = {};



void setup() {
  Serial.begin(9600);
  delay(300);

  // allocate memory for the audio library
  AudioMemory(8);
  audioShield.enable();
  audioShield.volume(0.8);

  // Initialize the filter
  myFilterL.begin(fir_list[0].coeffs, fir_list[0].num_coeffs); //Choose the first filter
  myFilterR.begin(fir_list[0].coeffs, fir_list[0].num_coeffs);
}


void loop()
{
  //the FIR filter function is interrupt based and is called as soon as 128 
  //data samples of audio input is available
  // read in the the coefficients from serial and build array
  // can make first number the size of the array
  // all others are coefficients, check iteration value by counting commas, pass value into second argument of filter.begin function
      if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingByte, DEC);
  }
  
}
