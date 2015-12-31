#include <Adafruit_NeoPixel.h>
#include <avr/power.h>
#include <Wire.h>

const byte magic[] = {0x48, 0x45, 0x58};
byte m_pos = 0;

byte data[] = {0x00, 0x00, 0x00, 0x00, 0x00};
byte d_pos = 0;

bool good_transmit = false;
bool new_data = true;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(16, 6, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  
  Wire.begin(16);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
}

void loop() {
  if (new_data)
    strip.show();
  delay(20);
}

void magic_ok(byte b) {
  if (magic[m_pos] == b) m_pos++; else m_pos = 0;
}

byte count_bits(byte b) {
  byte c = 0;
  for (byte i=0; i<8; i++) c += (b >> i) & 1;
  return c;
}

bool checksum_ok() {
  byte checksum = 0;
  for (byte i=0; i<4; i++) checksum += count_bits(data[i]);
  if (checksum == data[4]) return true; else return false;
}

void data_full() {
  if (checksum_ok()) {
    strip.setPixelColor(data[0], strip.Color(data[1], data[2], data[3]));
    good_transmit = true;
  }
  else {
    good_transmit = false;
  }
  
  m_pos = 0;
  d_pos = 0;
}

void feed_data(byte b) {
  if (d_pos < 5) {
    data[d_pos] = b;
    d_pos++;
  }
  if (d_pos > 4)
    data_full();
}

void receiveEvent(int count) {
  while (Wire.available()) {
    byte b = Wire.read();
    if (m_pos > 2)
      feed_data(b);
    else
      magic_ok(b);
  }
}

void requestEvent() {
  if (checksum_ok) Wire.write(0xf0); else Wire.write(0x0f);
}
