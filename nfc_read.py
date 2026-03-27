import board
import busio
from adafruit_pn532.i2c import PN532_I2C

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c)

pn532.SAM_configuration()

print("Kart okut...")

while True:
    uid = pn532.read_passive_target(timeout=1.0)
    if uid:
        print("KART ID:", [hex(i) for i in uid])