# Advanced Network Stress Testing Tool

**⚠️ EDUCATIONAL PURPOSE ONLY - FOR AUTHORIZED NETWORK TESTING ONLY ⚠️**

This tool is designed for educational research into network performance, congestion mechanics, and WiFi behavior under stress conditions. It implements various network stress testing techniques commonly used in network research and penetration testing.

## 🚨 IMPORTANT LEGAL NOTICE

**WARNING: Only use this tool on networks you own or have explicit written permission to test. Unauthorized use may violate laws, network policies, and terms of service. The authors are not responsible for misuse of this tool.**

## 📋 Features

### Stress Testing Methods

1. **UDP Flood** - Bandwidth saturation through connectionless packet flooding
2. **TCP SYN Flood** - Connection resource exhaustion via half-open connections  
3. **ICMP Flood** - Latency spike generation through ping flooding
4. **Mixed Protocol** - Realistic traffic patterns combining multiple protocols

### Advanced Capabilities

- Multi-threaded packet generation for maximum throughput
- Configurable packet rates and sizes
- Real-time statistics monitoring
- Source IP spoofing support (requires privileges)
- Graceful shutdown and comprehensive reporting
- Rate limiting to prevent system overload

## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- Linux/macOS/Windows (Linux recommended for full functionality)
- Root privileges (for TCP SYN flood and ICMP flood)

### Setup

1. Clone or download the tool:
```bash
git clone <repository> # or download files
cd network-stress-tester
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. For advanced features, install scapy:
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-scapy

# Or via pip
pip3 install scapy
```

4. Make the script executable:
```bash
chmod +x network_stress_tester.py
```

## 🚀 Usage

### Basic Usage

```bash
# Simple UDP flood test
python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types udp

# With rate limiting (1000 packets per second per thread)
python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types udp --pps 1000 --threads 5
```

### Advanced Examples

```bash
# Mixed protocol stress test
python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types mixed --threads 10 --duration 30

# TCP SYN flood (requires root)
sudo python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types tcp_syn --threads 20

# ICMP flood with custom packet size
sudo python3 network_stress_tester.py -t 192.168.1.1 --test-types icmp --packet-size 1500 --threads 15

# High-intensity multi-protocol test
sudo python3 network_stress_tester.py -t 192.168.1.1 -p 80 --test-types udp tcp_syn icmp --threads 25 --pps 2000
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target IP address (required) | - |
| `-p, --port` | Target port number | 80 |
| `--test-types` | Test types: udp, tcp_syn, icmp, mixed | udp |
| `--threads` | Number of threads per test type | 10 |
| `--packet-size` | Packet size in bytes | 1024 |
| `--pps` | Packets per second per thread (0=unlimited) | 0 |
| `--duration` | Test duration in seconds (0=until Ctrl+C) | 0 |
| `--spoof-ip` | Enable source IP spoofing | False |
| `-v, --verbose` | Verbose output | False |

## 📊 Understanding the Output

### Real-time Statistics

```
[15.2s] Packets: 45,230 | Rate: 2,975.7 pps | Bandwidth: 23.81 Mbps | Errors: 0 | Threads: 12
```

- **Packets**: Total packets sent
- **Rate**: Current packets per second
- **Bandwidth**: Current bandwidth utilization
- **Errors**: Failed packet transmissions
- **Threads**: Active worker threads

### Final Report

```
============================================================
FINAL STATISTICS
============================================================
Duration:        30.00 seconds
Total Packets:   89,450
Total Bytes:     91,596,800 (87.35 MB)
Average PPS:     2,981.7
Average Mbps:    24.42
Errors:          0
Success Rate:    100.0%
============================================================
```

## 🧠 Educational Concepts

### Network Congestion Mechanics

This tool demonstrates several key network concepts:

#### 1. Bandwidth Saturation (UDP Flood)
- **Concept**: Overwhelming available bandwidth with data
- **Effect**: Legitimate traffic experiences delays and packet loss
- **Real-world**: Video streaming degradation, file transfer slowdowns

#### 2. Connection Exhaustion (TCP SYN Flood)
- **Concept**: Consuming server connection resources
- **Effect**: Server cannot accept new legitimate connections
- **Real-world**: Web server becomes unresponsive to new users

#### 3. Processing Overhead (ICMP Flood)
- **Concept**: Forcing target to process many small requests
- **Effect**: CPU and network stack become overwhelmed
- **Real-world**: Router/switch performance degradation

### WiFi-Specific Impacts

WiFi networks are particularly vulnerable to these attacks because:

1. **Shared Medium**: All devices compete for the same radio spectrum
2. **Half-Duplex**: Cannot send and receive simultaneously
3. **Collision Domain**: Interference affects all connected devices
4. **Limited Bandwidth**: Typically much lower than wired connections

### Performance Bottlenecks

Common bottlenecks this tool can help identify:

- **Router/AP Processing Power**: CPU limitations handling packet processing
- **Network Interface Limits**: Maximum packets per second capabilities  
- **Buffer Overflow**: Queue saturation causing packet drops
- **Protocol Stack Overhead**: OS networking layer performance limits

## 🛡️ Defensive Measures

Understanding these attacks helps implement proper defenses:

### Network-Level Protections
- **Rate Limiting**: Restrict packets per second from single sources
- **SYN Cookies**: Mitigate TCP SYN flood attacks
- **ICMP Rate Limiting**: Reduce ICMP processing overhead
- **Traffic Shaping**: Prioritize legitimate traffic

### Infrastructure Hardening
- **Firewall Rules**: Block suspicious traffic patterns
- **Intrusion Detection**: Monitor for attack signatures
- **Load Balancing**: Distribute traffic across multiple servers
- **DDoS Protection**: Cloud-based mitigation services

## 🔬 Research Applications

This tool is valuable for:

### Network Performance Research
- Measuring WiFi performance under stress
- Analyzing congestion control algorithms
- Testing Quality of Service (QoS) implementations
- Evaluating network equipment capabilities

### Security Research
- Understanding attack vectors and impacts
- Testing defensive mechanisms
- Analyzing network resilience
- Developing mitigation strategies

### Educational Purposes
- Demonstrating network concepts in practice
- Training network administrators
- Cybersecurity education and awareness
- Protocol behavior analysis

## ⚠️ Safety and Ethical Guidelines

### Authorized Testing Only
- Only test networks you own or have explicit permission to test
- Obtain written authorization before testing third-party networks
- Respect network policies and terms of service
- Consider impact on other network users

### Responsible Disclosure
- Report vulnerabilities through proper channels
- Allow reasonable time for fixes before public disclosure
- Provide constructive feedback to network operators
- Document findings for educational purposes

### Rate Limiting Recommendations
- Start with low packet rates (100-1000 pps)
- Monitor target system resources
- Use duration limits to prevent extended outages
- Have emergency stop procedures ready

## 🐛 Troubleshooting

### Common Issues

**Permission Denied Errors**
```bash
# Solution: Run with sudo for raw sockets
sudo python3 network_stress_tester.py ...
```

**Scapy Import Errors**
```bash
# Solution: Install scapy
pip3 install scapy
# or
sudo apt-get install python3-scapy
```

**High CPU Usage**
```bash
# Solution: Reduce thread count or add rate limiting
--threads 5 --pps 1000
```

**Network Unreachable**
```bash
# Solution: Verify target IP and network connectivity
ping 192.168.1.1
```

### Performance Optimization

- Use rate limiting to prevent system overload
- Adjust thread count based on system capabilities
- Monitor system resources during testing
- Use appropriate packet sizes for test objectives

## 📚 References

### Networking Concepts
- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol  
- RFC 792: Internet Control Message Protocol
- IEEE 802.11: WiFi Standards

### Security Research
- NIST Cybersecurity Framework
- OWASP Testing Guide
- Common Vulnerabilities and Exposures (CVE)
- Network Security Best Practices

## 📝 License

This tool is provided for educational and research purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally.**