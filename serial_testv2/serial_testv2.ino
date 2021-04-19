void setup() {
    Serial.begin(9600);
}

void loop() {
    static float buffer[5];
    static size_t pos;
    if (Serial.available()) {
        char c = Serial.read();
        if (c == ',') {  // on end of line, parse the number
            buffer[pos] = '\0';
            float value = atof(buffer);
            Serial.print("received: ");
            Serial.println(value);
            pos = 0;
        } else if (pos < sizeof buffer - 1) {  // otherwise, buffer it
            buffer[pos++] = c;
        }
    }
}