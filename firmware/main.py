# Import board pins
import board

# KMK imports
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros

# Create keyboard instance
keyboard = KMKKeyboard()

# Add macro support
macros = Macros()
keyboard.modules.append(macros)

# Define your GPIO pins 
PINS = [board.D26, board.D27, board.D0, board.D1, board.D2, board.D3]

# Tell KMK we're using individual pins (not a matrix)
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Here you define the buttons corresponding to the pins
# Will be changed and defined later after Macropad is built
keyboard.keymap = [
    [KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO]
]

# Start the keyboard!
if __name__ == '__main__':
    keyboard.go()