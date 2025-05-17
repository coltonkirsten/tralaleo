#!/usr/bin/env python3
"""
send.py - Improved Morse code LED transmitter

Usage:
./send.py <count> "<message>" [--rate RATE] [--preamble] [--debug]

<count>    Number of times to repeat the message
<message>  The message to send (letters, digits, spaces)
--rate     Duration of one DOT in seconds (default: 0.5)
--preamble Send a preamble sequence to help calibrate the receiver
--debug    Print timing information during transmission
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

def blink(duration, debug=False):
    """Blink the LED for the specified duration"""
    if debug:
        print(f"ON for {duration:.2f}s")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PIN, GPIO.LOW)

def send_preamble(dot_dur, debug=False):
    """Send a calibration sequence to help the receiver"""
    # Send a preamble pattern: 3 dots with proper spacing
    if debug:
        print("Sending preamble...")
    
    # Long initial gap to ensure we're starting from clean state
    time.sleep(dot_dur * 5)
    
    # Send 3 dots with standard timing
    for _ in range(3):
        blink(dot_dur, debug)
        time.sleep(dot_dur)  # Symbol gap
    
    # Add extra gap before the actual message
    time.sleep(dot_dur * 3)
    
    if debug:
        print("Preamble complete")

def send_message(msg, dot_dur, debug=False):
    """Send a message in Morse code"""
    dash_dur   = dot_dur * 3
    sym_gap    = dot_dur
    letter_gap = dot_dur * 3
    word_gap   = dot_dur * 7
    
    # Convert message to uppercase
    msg = msg.upper()
    
    if debug:
        print(f"Sending message: '{msg}' with dot duration: {dot_dur}s")
    
    for ch in msg:
        code = MORSE_CODE.get(ch, '')
        if debug:
            print(f"Character: {ch}, Morse: {code}")
        
        if code == '/':
            if debug:
                print(f"Word gap: {word_gap:.2f}s")
            time.sleep(word_gap)
            continue
            
        if not code:
            continue  # skip unknown characters
            
        for i, sym in enumerate(code):
            if sym == '.':
                blink(dot_dur, debug)
                if debug:
                    print("DOT")
            else:  # sym == '-'
                blink(dash_dur, debug)
                if debug:
                    print("DASH")
                
            # Add symbol gap except after the last symbol of this character
            if i < len(code) - 1:
                if debug:
                    print(f"Symbol gap: {sym_gap:.2f}s")
                time.sleep(sym_gap)
        
        # Add letter gap after each character
        if debug:
            print(f"Letter gap: {letter_gap:.2f}s")
        time.sleep(letter_gap)

def main():
    p = argparse.ArgumentParser(description="Improved Morse LED sender")
    p.add_argument("count", type=int, help="Repetition count")
    p.add_argument("message", type=str, help="Text to transmit")
    p.add_argument("--rate", type=float, default=0.5,
                   help="DOT duration in seconds")
    p.add_argument("--preamble", action="store_true",
                   help="Send calibration preamble")
    p.add_argument("--debug", action="store_true",
                   help="Print timing information")
    args = p.parse_args()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

    try:
        print(f"Starting transmission of '{args.message}' {args.count} time(s)")
        
        for i in range(args.count):
            if i > 0:
                print(f"\nRepetition {i+1}/{args.count}")
                # Add extra gap between repetitions
                time.sleep(args.rate * 10)
                
            if args.preamble:
                send_preamble(args.rate, args.debug)
                
            send_message(args.message, args.rate, args.debug)
            
        print("\nTransmission complete")
        
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()