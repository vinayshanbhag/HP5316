#!/usr/bin/env python
import pyvisa
import sys
from PIL import Image
from io import BytesIO
from datetime import datetime

def main():  
    if len(sys.argv[1:]) != 2:
        print("screenshot.py\nTake screenshot from Siglent oscilloscope and save image to local disk.\nImage format is specified by the file extension (.png/.jpg/.bmp)\nUsage:\nscreenshot.py ip_address output_filename")
        exit()
    
    ip = sys.argv[1]
    output_filename = sys.argv[2]
    filename_and_path = '.'.join(output_filename.split('.')[:-1])
    extension = output_filename.split('.')[-1]
    rm = pyvisa.ResourceManager()
    try:
        print("Connecting...")
        dev = rm.open_resource(f"TCPIP::{ip}::INSTR")
        print(f"Connected to {dev.query('*IDN?').strip()}")
    except:
        print(f"Failed to connect to device at {ip}")
        exit()
    dev.chunk_size = 20*1024*1024
    dev.write("SCDP")
    str = dev.read_raw()
    im = Image.open(BytesIO(str))

    im.save(f"{filename_and_path}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{extension}")
    

if __name__ == "__main__":
    main()