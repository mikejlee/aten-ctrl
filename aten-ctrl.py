#!/usr/bin/env python3

import serial
import time
import argparse
import logging

# ---- Configuration ----
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 38400
TIMEOUT = 1  # seconds
ENCODING = 'ascii'

# ---- Setup Logging ----
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# ---- Command Definitions ----
COMMANDS = {
    "next": b"sw\r",
    "info": b"info\r",
    "port": lambda x: f"sw p0{x}\r".encode(ENCODING),
}

# ---- Serial Communication ----
def send_command(cmd_bytes):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            logging.debug(f"Sending: {cmd_bytes}")
            ser.write(cmd_bytes)
            time.sleep(0.1)
            response = ser.read(100)
            logging.debug(f"Raw Bytes: {response}")
            decoded = response.decode(ENCODING, errors='ignore').strip()
            logging.info(f"Response: {decoded}")
    except serial.SerialException as e:
        logging.error(f"Serial error: {e}")
        return None
    return decoded

# ---- Argument Parser ----
def parse_args():
    parser = argparse.ArgumentParser(description="ATEN US3344I RS485 Control")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--next", action="store_true", help="Switch to next port")
    group.add_argument("--port", type=int, choices=[1, 2, 3, 4], help="Switch to port number")
    group.add_argument("--info", action="store_true", help="Display firmware info")
    return parser.parse_args()

# ---- Main ----
def main():
    args = parse_args()
    
    if args.next:
        send_command(COMMANDS["next"])
    elif args.info:
        send_command(COMMANDS["info"])
    elif args.port:
        cmd = COMMANDS["port"](args.port)
        send_command(cmd)

if __name__ == "__main__":
    main()