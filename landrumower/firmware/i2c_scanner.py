from machine import I2C, Pin
import time

def scan_i2c():
    # I2C0 inicializálása
    i2c0 = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    
    print("I2C eszközök keresése...")
    print("Cím\tHex\tDec")
    print("-" * 30)
    
    # I2C0 eszközeinek keresése
    devices = i2c0.scan()
    
    if not devices:
        print("Nem található I2C eszköz!")
    else:
        for device in devices:
            print(f"0x{device:02X}\t{device:02X}\t{device}")

if __name__ == "__main__":
    scan_i2c() 