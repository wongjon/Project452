/*

*/

#define HWSERIAL Serial1

void setup() {
    
}

void loop() {


  float coefficient[5];
  int tmp1 = 1;
  int tmp2 = 1;
  int tmp3 = 1;
  int tmp4 = 1;

  if(HWSERIAL.available() >0) {
    for(int i = 0; i < 5; i++) {
      for(int j = 0; j < 4; j++) {

        byte incomingByte = HWSERIAL.read();

        if(j == 0) {
          int tmp1 = sizeof(incomingByte);
          memcpy(coefficient[i], incomingByte, tmp1);
        }

        else if(j == 1) {
          int tmp2 = sizeof(incomingByte);
          memcpy(coefficient[i] + tmp1, incomingByte, tmp2);
        }

        else if(j == 2) {
          int tmp3 = sizeof(incomingByte);
          memcpy(coefficient[i] + tmp1 + tmp2, incomingByte, tmp3);

        }

        else if(j == 3) {
          int tmp4 = sizeof(incomingByte);
          memcpy(coefficient[i] + tmp1 + tmp2 + tmp3, incomingByte, tmp4);
        }

      }
      
      printf(coefficient[i]);
      
    }
  }
}
