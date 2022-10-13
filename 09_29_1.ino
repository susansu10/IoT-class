// C++ code
//
int button = 0;

int LED = 0;

int END = 0;

int value = 0;

void setup()
{
  pinMode(A0, INPUT);
  Serial.begin(9600);
  pinMode(7, INPUT);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop()
{
  value = analogRead(A0);
  Serial.println(value);
  if (digitalRead(7) == 1) {
    button = 1;
    while (digitalRead(7) == 1) {
    }
  } else {
    button = 0;
  }
  if (LED > 2) {
    LED = 0;
  }
  if (button == 1 && END == 0) {
    LED = (LED + 1);
    Serial.println(LED);
  }
  LED = (LED % 3);
  if (button == 1) {
    if (LED == 1) {
      analogWrite(3, value);
    } else {
      analogWrite(3, 0);
    }
    if (LED == 2) {
      analogWrite(5, value);
    } else {
      analogWrite(5, 0);
    }
    if (LED == 0) {
      analogWrite(6, value);
    } else {
      analogWrite(6, 0);
    }
  } else {
    analogWrite(3, 0);
    analogWrite(5, 0);
    analogWrite(6, 0);
  }
  delay(10); // Delay a little bit to improve simulation performance
}