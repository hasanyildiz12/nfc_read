#!/usr/bin/env python3
import board
import busio
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()

print("NFC kartını okutun...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid:
        print("Kart ID:", uid.hex())