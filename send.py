#!/usr/bin/env python3
"""
send.py - Morse code LED transmitter

Usage:
    ./send.py <count> "<message>" [--rate RATE]

    <count>    Number of times to repeat the message
    <message>  The message to send (letters, digits, spaces)
    --rate     Duration of one DOT in seconds (default: 0.05)
"""

import argparse
import time
import RPi.GPIO as GPIO

# GPIO pin where the LED is connected
LED_PIN = 17

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
    ' ': '/'  # placeholder for word gap
}

def blink(duration):
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)

def send_message(msg, dot_dur):
    dash_dur   = dot_dur * 3
    sym_gap    = dot_dur
    letter_gap = dot_dur * 3
    word_gap   = dot_dur * 7

    for ch in msg.upper():
        code = MORSE_CODE.get(ch, '')
        if code == '/':
            time.sleep(word_gap)
            continue
        if not code:
            continue  # skip unknown characters
        for sym in code:
            blink(dot_dur if sym == '.' else dash_dur)
            time.sleep(sym_gap)
        time.sleep(letter_gap - sym_gap)

def main():
    p = argparse.ArgumentParser(description="Morse LED sender")
    p.add_argument("count",  type=int,   help="Repetition count")
    p.add_argument("message",type=str,   help="Text to transmit")
    p.add_argument("--rate", type=float, default=0.05,
                   help="DOT duration in seconds")
    args = p.parse_args()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

    try:
        for _ in range(args.count):
            send_message(args.message, args.rate)
            time.sleep(args.rate * 7)  # word gap between repeats
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()