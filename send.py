#!/usr/bin/env python3
"""
send.py

Usage:
    ./send.py <count> "<message>"

Example:
    ./send.py 4 "hello ESP32"
"""
import sys
import time
import RPi.GPIO as GPIO

# GPIO pin where the LED is connected
LED_PIN = 17

# Timing definitions (seconds)
DOT_DURATION   = 0.2
DASH_DURATION  = DOT_DURATION * 3
SYMBOL_GAP     = DOT_DURATION      # between dots/dashes
LETTER_GAP     = DOT_DURATION * 3  # between letters
WORD_GAP       = DOT_DURATION * 7  # between words

# Morse code mapping
MORSE_CODE = {
    'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',  'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',  'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',  'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',  'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----',
    ' ': '/'  # we'll treat '/' as word separator
}

def blink_dot():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(DOT_DURATION)
    GPIO.output(LED_PIN, GPIO.LOW)

def blink_dash():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(DASH_DURATION)
    GPIO.output(LED_PIN, GPIO.LOW)

def send_message(message):
    for char in message:
        code = MORSE_CODE.get(char.upper(), '')
        if code == '/':
            # word gap
            time.sleep(WORD_GAP)
            continue
        if not code:
            # unknown character, skip
            continue
        for symbol in code:
            if symbol == '.':
                blink_dot()
            elif symbol == '-':
                blink_dash()
            # gap between symbols
            time.sleep(SYMBOL_GAP)
        # gap between letters (already waited one SYMBOL_GAP after last symbol)
        time.sleep(LETTER_GAP - SYMBOL_GAP)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <count> \"<message>\"")
        sys.exit(1)

    try:
        count = int(sys.argv[1])
    except ValueError:
        print("First argument must be an integer (number of times).")
        sys.exit(1)
    message = sys.argv[2]

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

    try:
        for i in range(count):
            send_message(message)
            # small pause between repetitions
            time.sleep(WORD_GAP)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()