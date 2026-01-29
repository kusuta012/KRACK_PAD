import board
import neopixel
import time
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Macros, Tap, Press, Release, Delay

# 1. Initialize Keyboard and Macros
keyboard = KMKKeyboard()
macros = Macros()
keyboard.modules.append(macros)

# 2. Setup NeoPixel
status_led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5)

def wheel(pos):
    if pos < 85: return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

class RainbowLED:
    def __init__(self, pixel):
        self.pixel = pixel
        self.pos = 0
        self.last_update = time.monotonic()
    def update(self):
        now = time.monotonic()
        if now - self.last_update > 0.020:
            self.pixel.fill(wheel(self.pos))
            self.pos = (self.pos + 1) % 256
            self.last_update = now

rainbow = RainbowLED(status_led)

# --- MACRO DEFINITIONS ---

# SW1: Win+R -> "code" -> Enter
OPEN_VSCODE = KC.MACRO(
    Press(KC.LWIN), Tap(KC.R), Release(KC.LWIN),
    Delay(200),
    "code",
    Tap(KC.ENT)
)

# SW2: Show Desktop (Win + D)
SHOW_DESKTOP = KC.LWIN(KC.D)

# SW3: Task Manager (Ctrl + Shift + Esc)
TASK_MANAGER = KC.LCTL(KC.LSFT(KC.ESC))

# SW4: Lock PC (Win + L)
LOCK_PC = KC.LWIN(KC.L)

# SW5: Git Status
GIT_STATUS = KC.MACRO("git status", Tap(KC.ENT))

# SW6: Git Commit with cursor move
GIT_COMMIT = KC.MACRO("git commit -m \"\"", Tap(KC.LEFT))

# --- KEYBOARD SETUP ---

PINS = [board.TX, board.RX, board.SCK, board.MOSI, board.A0, board.A1]
keyboard.matrix = KeysScanner(pins=PINS, value_when_pressed=False)

keyboard.keymap = [
    [
        OPEN_VSCODE,    # SW1
        SHOW_DESKTOP,   # SW2
        TASK_MANAGER,   # SW3
        LOCK_PC,        # SW4
        GIT_STATUS,     # SW5
        GIT_COMMIT      # SW6
    ]
]

def before_matrix_scan_with_rainbow():
    rainbow.update()

keyboard.before_matrix_scan = before_matrix_scan_with_rainbow

if __name__ == '__main__':
    keyboard.go()
