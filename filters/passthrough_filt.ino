#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

const int myInput = AUDIO_INPUT_LINEIN;


AudioInputI2S         audioInput;         // audio shield: mic or line-in
AudioOutputI2S        audioOutput;        // audio shield: headphones & line-out

/*
// GUItool: begin automatically generated code
AudioInputI2S            i2s1;           //xy=413,275
AudioOutputI2S           i2s2;           //xy=648,277
AudioConnection          patchCord1(i2s1, 0, i2s2, 0);
AudioConnection          patchCord2(i2s1, 1, i2s2, 1);
AudioControlSGTL5000     sgtl5000_1;     //xy=551,396
// GUItool: end automatically generated code
*/

void setup() {
  Serial.begin(9600);
  delay(300);
  pinMode(LED, OUTPUT);

  // allocate memory for the audio library
  AudioMemory(8);
  audioShield.enable();
  audioShield.volume(0.6);
}
