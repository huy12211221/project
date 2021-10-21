void setup() 
{
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);

    Serial.begin(9600);
    Serial.println("Serial connected");
}

void loop() 
{
    int c;
    if (Serial.available() > 0) 
    {
        // read the incoming byte:
        c = Serial.read();
    }
    if (c == 49)
    {
        digitalWrite(LED_BUILTIN, HIGH);
    }
    else if (c == 48)
    {
        digitalWrite(LED_BUILTIN, LOW);
    }

}
