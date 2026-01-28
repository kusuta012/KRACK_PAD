import board
import neopixel
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
# 1. Wait a moment for the board to settle
time.sleep(1)
# 2. Setup NeoPixel - brightness can be 0.0 to 1.0
status_led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.03)  # Very dim
# Rainbow color wheel function
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
# Rainbow animation in background
class RainbowLED:
    def __init__(self, pixel):
        self.pixel = pixel
        self.pos = 0
        self.last_update = time.monotonic()
    def update(self):
        now = time.monotonic()
        if now - self.last_update > 0.020:  # Update every 20ms
            self.pixel.fill(wheel(self.pos))
            self.pos = (self.pos + 1) % 256
            self.last_update = now
rainbow = RainbowLED(status_led)
keyboard = KMKKeyboard()
# SW1:D6/TX, SW2:D7/RX, SW3: D8/SCK, SW4:D10/MOSI, SW5:ANALOG0, SW6:ANALOG1
PINS = [board.TX, board.RX, board.SCK, board.MOSI, board.A0, board.A1]
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)
keyboard.keymap = [
    [KC.A, KC.B, KC.C, KC.D, KC.E, KC.F]
]
# Hook into KMK's main loop to update rainbow
def before_matrix_scan_with_rainbow():
    rainbow.update()
keyboard.before_matrix_scan = before_matrix_scan_with_rainbow
if __name__ == '__main__':
    keyboard.go()

