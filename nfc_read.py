from smbus2 import SMBus
import time

PN532_ADDR = 0x24

def write_command(bus, cmd, params=[]):
    frame = [0x00, 0x00, 0xFF]
    length = len(params) + 2
    frame += [length, (~length & 0xFF), 0xD4, cmd]
    frame += params

    checksum = 0xD4 + cmd + sum(params)
    frame += [(~checksum & 0xFF), 0x00]

    bus.write_i2c_block_data(PN532_ADDR, 0x00, frame)

def read_ack(bus):
    time.sleep(0.1)
    ack = bus.read_i2c_block_data(PN532_ADDR, 0x00, 6)
    return ack == [0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00]

def read_response(bus, length=32):
    time.sleep(0.2)
    return bus.read_i2c_block_data(PN532_ADDR, 0x00, length)

def sam_config(bus):
    write_command(bus, 0x14, [0x01, 0x14, 0x01])
    read_ack(bus)

def read_uid(bus):
    write_command(bus, 0x4A, [0x01, 0x00])
    if not read_ack(bus):
        return None

    data = read_response(bus)

    # DEBUG için:
    print("RAW:", data)

    # UID parse (daha doğru offset)
    try:
        if data[7] != 0xD5:
            return None
        if data[8] != 0x4B:
            return None

        uid_length = data[13]
        uid = data[14:14+uid_length]
        return uid
    except:
        return None

def main():
    bus = SMBus(1)

    print("PN532 init...")
    sam_config(bus)

    print("Kart okut...")

    while True:
        uid = read_uid(bus)
        if uid:
            print("KART ID:", [hex(x) for x in uid])
            time.sleep(1)

if __name__ == "__main__":
    main()