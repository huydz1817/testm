#!/usr/bin/env python3
"""
Network Stress Testing Examples
==============================

This file demonstrates various usage scenarios for the network stress testing tool.
Each example shows different aspects of network behavior under stress conditions.

EDUCATIONAL PURPOSE ONLY - FOR AUTHORIZED NETWORK TESTING ONLY
"""

import subprocess
import time
import sys
import os

def run_command(cmd, description):
    """Execute a command with description"""
    print(f"\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("\nPress Enter to run this example (Ctrl+C to skip)...")
    
    try:
        input()
        print(f"\nRunning: {cmd}")
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\nSkipped.")

def main():
    """Main function demonstrating various stress test scenarios"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              NETWORK STRESS TESTING EXAMPLES                 ║
║                 EDUCATIONAL USE ONLY                         ║
╠══════════════════════════════════════════════════════════════╣
║  These examples demonstrate different network stress         ║
║  scenarios for educational and research purposes.            ║
║                                                              ║
║  WARNING: Only use on authorized networks!                   ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check if the main script exists
    if not os.path.exists("network_stress_tester.py"):
        print("Error: network_stress_tester.py not found in current directory")
        sys.exit(1)
    
    target_ip = input("Enter target IP address for testing (e.g., 192.168.1.1): ")
    
    if not target_ip:
        print("Error: Target IP is required")
        sys.exit(1)
    
    print(f"\nTarget set to: {target_ip}")
    print("\nThe following examples will be demonstrated:")
    
    examples = [
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types udp --threads 5 --pps 500 --duration 10",
            "desc": "Light UDP Flood - Basic bandwidth testing"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types udp --threads 15 --pps 2000 --duration 15",
            "desc": "Heavy UDP Flood - Bandwidth saturation testing"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types tcp_syn --threads 10 --pps 1000 --duration 10",
            "desc": "TCP SYN Flood - Connection exhaustion (requires root)"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} --test-types icmp --threads 8 --pps 800 --duration 10",
            "desc": "ICMP Flood - Latency spike generation (requires root)"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types mixed --threads 12 --pps 1500 --duration 20",
            "desc": "Mixed Protocol - Realistic traffic simulation"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types udp --threads 20 --packet-size 64 --pps 5000 --duration 15",
            "desc": "Small Packet Flood - High PPS testing"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types udp --threads 10 --packet-size 1500 --pps 1000 --duration 15",
            "desc": "Large Packet Flood - MTU-sized packet testing"
        },
        {
            "cmd": f"python3 network_stress_tester.py -t {target_ip} -p 80 --test-types udp tcp_syn icmp --threads 8 --pps 800 --duration 25",
            "desc": "Multi-Protocol Simultaneous - Combined attack vectors (requires root)"
        }
    ]
    
    for example in examples:
        run_command(example["cmd"], example["desc"])
    
    print(f"\n{'='*60}")
    print("EXAMPLES COMPLETED")
    print(f"{'='*60}")
    print("\nKey Learning Points:")
    print("- Different protocols create different network effects")
    print("- Packet size affects bandwidth vs. processing load")
    print("- Thread count impacts system resources")
    print("- Rate limiting prevents system overload")
    print("- Mixed protocols simulate realistic scenarios")
    print("\nFor more advanced usage, see the README.md file.")

if __name__ == "__main__":
    main()