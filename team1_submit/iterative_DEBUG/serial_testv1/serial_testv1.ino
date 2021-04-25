#include <Audio.h>
#include <Wire.h>
#include <SD.h>
#include <SPI.h>
#include <SerialFlash.h>




void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

String incomingByte;
int arr[11];

void loop() {
  int size = 0;
  int j = 0;
  String tmp;
  int val = 0;
  char t;

  while (Serial.available()) {
    if (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.readString();

      // say what you got:

    }

    Serial.print("I received: ");
    //Serial.print(incomingByte);
    size = incomingByte.length();
    //Serial.println(size);
    for(int i = 0; i < size; i++){
      Serial.print(incomingByte[i]);
      Serial.print(' ,');
    }
    /*for (int i = 0; i < size; i++) {
      while (j < 100) {
        if (incomingByte[i] == ',') {
          val = tmp.toInt();
          arr[j] = val;
          Serial.print(arr[j]);
          j++;
        }
        else {
          t = incomingByte[i];
          tmp = tmp + t;
          Serial.print(tmp);
        }
      }
    }
    */
  }






  /*if (Serial.available() > 0) {
    coeffs[idx] = Serial.parseInt();
        Serial.print("Received new angle: ");
        coeffs[idx-1] = 0;
        Serial.println(coeffs);
        idx = -1;
    idx++;
    }*/
}
