#!/usr/bin/env python3
"""
Network Capture Utility
A script to automate network captures using Wireshark/tshark
"""

import argparse
import subprocess
import datetime
import os
import sys

def setup_capture(interface, duration, output_file):
    """
    Set up and run a network capture using tshark
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_file:
        output_file = f"capture_{timestamp}.pcap"
    
    # Construct tshark command
    command = [
        "tshark",
        "-i", interface,
        "-w", output_file,
        "-a", f"duration:{duration}"
    ]
    
    print(f"Starting capture on interface {interface}")
    print(f"Capture will run for {duration} seconds")
    print(f"Saving to {output_file}")
    
    try:
        subprocess.run(command, check=True)
        print(f"\nCapture completed successfully")
        print(f"Capture file saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during capture: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Automated network capture utility")
    parser.add_argument("-i", "--interface", required=True,
                      help="Network interface to capture on")
    parser.add_argument("-d", "--duration", type=int, default=60,
                      help="Duration of capture in seconds (default: 60)")
    parser.add_argument("-o", "--output", 
                      help="Output file name (default: capture_TIMESTAMP.pcap)")
    
    args = parser.parse_args()
    
    # Check if running with sufficient privileges
    if os.geteuid() != 0:
        print("This script requires root privileges to capture network traffic")
        print("Please run with sudo")
        sys.exit(1)
    
    setup_capture(args.interface, args.duration, args.output)

if __name__ == "__main__":
    main()