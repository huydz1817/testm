# Network Stress Testing Tool - No Root Required

**⚠️ EDUCATIONAL PURPOSE ONLY - FOR AUTHORIZED NETWORK TESTING ONLY ⚠️**

This is a specialized version of the network stress testing tool that works **without requiring root privileges** while still providing effective network stress testing capabilities for WiFi performance research and educational purposes.

## 🚨 IMPORTANT LEGAL NOTICE

**WARNING: Only use this tool on networks you own or have explicit written permission to test. Unauthorized use may violate laws, network policies, and terms of service.**

## 🔑 Key Advantages - No Root Required

Unlike the full version that requires root privileges for raw socket access, this version:

✅ **Works with standard user privileges**  
✅ **No sudo/administrator access needed**  
✅ **Still creates significant network stress**  
✅ **Portable across different systems**  
✅ **Safer for educational environments**  

## 📋 Available Stress Testing Methods

### 1. UDP Flood (`udp`) - **Most Effective for Bandwidth Saturation**
- **How it works**: Uses standard UDP sockets (no raw sockets needed)
- **Effect**: Saturates network bandwidth with high-volume packet flooding
- **WiFi Impact**: Causes severe congestion, packet loss, and performance degradation
- **Why no root needed**: Uses `socket.SOCK_DGRAM` instead of raw sockets

```bash
# High-intensity UDP flood
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types udp --threads 20 --pps 3000
```

### 2. TCP Connection Flood (`tcp_connect`) - **Connection Exhaustion**
- **How it works**: Creates real TCP connections (full 3-way handshake)
- **Effect**: Exhausts server connection resources and file descriptors
- **WiFi Impact**: Overloads router connection tables, affects all devices
- **Advantage**: Works through firewalls and NAT

```bash
# TCP connection exhaustion
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types tcp_connect --threads 25
```

### 3. System Ping Flood (`ping`) - **Latency Spike Generation**
- **How it works**: Uses system `ping` command via subprocess
- **Effect**: Creates processing overhead and latency spikes
- **WiFi Impact**: Consumes router CPU, increases response times
- **Cross-platform**: Works on Windows, Linux, and macOS

```bash
# Ping flood for latency testing
python3 network_stress_tester_noroot.py -t 192.168.1.1 --test-types ping --threads 15 --pps 500
```

### 4. HTTP Request Flood (`http`) - **Application Layer Stress**
- **How it works**: Sends rapid HTTP GET requests to web servers
- **Effect**: Tests application-layer performance and server capacity
- **WiFi Impact**: Creates realistic web traffic load patterns
- **Realistic**: Simulates actual user traffic

```bash
# HTTP application stress
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types http --threads 30
```

### 5. Mixed Protocol (`mixed`) - **Comprehensive Testing**
- **How it works**: Randomly combines all above methods
- **Effect**: Creates realistic mixed-traffic scenarios
- **WiFi Impact**: Tests network under varied load conditions
- **Research Value**: Most representative of real-world conditions

```bash
# Mixed protocol comprehensive test
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types mixed --threads 20 --duration 60
```

## 🚀 Quick Start Examples

### Basic WiFi Stress Test
```bash
# Simple bandwidth saturation test
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types udp --threads 10 --pps 1000 --duration 30
```

### High-Intensity WiFi Congestion
```bash
# Maximum stress test for severe lag simulation
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types udp tcp_connect --threads 25 --pps 5000 --duration 60
```

### Router Performance Testing
```bash
# Test router under mixed realistic load
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types mixed --threads 15 --pps 2000 --duration 120
```

### Application Server Stress
```bash
# Test web server performance
python3 network_stress_tester_noroot.py -t 192.168.1.1 -p 80 --test-types http --threads 50 --pps 100
```

## 📊 Real-Time Monitoring Output

```
[45.3s] Packets: 127,450 | Connections: 8,234 | Rate: 2,814.7 pps | Bandwidth: 22.52 Mbps | Errors: 12 | Threads: 25
```

**Metrics Explained:**
- **Packets**: Total packets/requests sent
- **Connections**: Successful TCP connections established  
- **Rate**: Current packets per second
- **Bandwidth**: Current bandwidth utilization
- **Errors**: Failed transmissions
- **Threads**: Active worker threads

## 🧠 Educational Value - WiFi Performance Research

### Understanding WiFi Congestion
This tool helps demonstrate key WiFi vulnerabilities:

#### 1. **Shared Medium Effect**
- All WiFi devices share the same radio spectrum
- High traffic from one device affects all connected devices
- Demonstrates why WiFi performance degrades with more users

#### 2. **Half-Duplex Limitations**  
- WiFi cannot send and receive simultaneously
- Shows how bidirectional traffic creates bottlenecks
- Explains WiFi's inherent performance limitations

#### 3. **Collision Domain Impact**
- All devices in WiFi range compete for airtime
- Demonstrates how interference affects entire network
- Shows why physical proximity matters in WiFi performance

#### 4. **Router Resource Exhaustion**
- Limited CPU and memory in consumer routers
- Connection table overflow effects
- Buffer saturation and packet dropping

### Measurable WiFi Performance Effects

**What you'll observe during testing:**

🔴 **Bandwidth Saturation**
- Download/upload speeds drop significantly
- Streaming video stutters or stops
- File transfers slow to crawl

🔴 **Latency Spikes**  
- Ping times increase from <10ms to 100ms+
- Web page loading becomes sluggish
- Online gaming becomes unplayable

🔴 **Connection Issues**
- Devices may disconnect and reconnect
- New devices can't join the network
- Existing connections become unstable

🔴 **Router Instability**
- Admin interface becomes unresponsive
- Router may require restart
- LED indicators show error states

## 🛡️ Defensive Research Applications

Understanding these attacks helps implement proper WiFi security:

### Network Monitoring
- **Traffic Analysis**: Identify abnormal traffic patterns
- **Bandwidth Monitoring**: Set alerts for unusual usage
- **Connection Tracking**: Monitor connection establishment rates

### Quality of Service (QoS)
- **Traffic Prioritization**: Ensure critical traffic gets bandwidth
- **Rate Limiting**: Prevent single devices from consuming all bandwidth  
- **Fair Queuing**: Distribute bandwidth fairly among users

### Infrastructure Hardening
- **Enterprise WiFi**: Use enterprise-grade access points
- **Load Balancing**: Distribute users across multiple access points
- **Bandwidth Management**: Implement per-user bandwidth limits

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Standard user account (no root/admin required)
- Network connectivity to target

### Installation
```bash
# Download the tool
wget https://raw.githubusercontent.com/your-repo/network_stress_tester_noroot.py

# Install dependencies
pip3 install psutil

# Make executable
chmod +x network_stress_tester_noroot.py

# Test installation
python3 network_stress_tester_noroot.py --help
```

## 📈 Performance Optimization Tips

### Maximizing Effectiveness Without Root

1. **Use Multiple Test Types Simultaneously**
   ```bash
   --test-types udp tcp_connect ping http
   ```

2. **Optimize Thread Count for Your System**
   ```bash
   # Start with CPU core count × 2-4
   --threads 16  # For 4-core system
   ```

3. **Adjust Packet Rate Based on Network Capacity**
   ```bash
   # For 100 Mbps network, try 2000-5000 pps
   --pps 3000
   ```

4. **Use Appropriate Packet Sizes**
   ```bash
   # Small packets for high PPS
   --packet-size 64 --pps 10000
   
   # Large packets for bandwidth saturation  
   --packet-size 1500 --pps 1000
   ```

## ⚠️ Responsible Usage Guidelines

### Educational Environment Safety
- **Start with low intensities** (--pps 100-500)
- **Use short durations** (--duration 10-30)
- **Monitor target system resources**
- **Have emergency stop procedures ready**

### Network Impact Considerations
- **Test during off-peak hours**
- **Warn other network users**
- **Monitor for service disruptions**
- **Be prepared to stop immediately**

### Legal and Ethical Compliance
- **Only test networks you own or have permission to test**
- **Document tests for educational purposes**
- **Report findings constructively**
- **Respect network policies and terms of service**

## 🐛 Troubleshooting

### Common Issues and Solutions

**High CPU Usage**
```bash
# Reduce thread count and add rate limiting
--threads 5 --pps 1000
```

**Connection Refused Errors**
```bash
# Target may be blocking connections, try different ports
-p 443  # or -p 22, -p 53
```

**Low Packet Rates**
```bash
# Remove rate limiting for maximum throughput
--pps 0  # Unlimited rate
```

**Memory Usage**
```bash
# Reduce packet size to lower memory usage
--packet-size 64
```

## 📚 Educational Resources

### Recommended Reading
- **WiFi Standards**: IEEE 802.11 specifications
- **Network Protocols**: TCP/UDP/ICMP fundamentals  
- **Network Security**: DoS/DDoS attack vectors and mitigation
- **Performance Analysis**: Network monitoring and optimization

### Practical Exercises
1. **Baseline Testing**: Measure normal network performance first
2. **Incremental Loading**: Gradually increase test intensity
3. **Protocol Comparison**: Compare effects of different test types
4. **Mitigation Testing**: Test effectiveness of defensive measures

## 🎯 Research Questions to Explore

- How does packet size affect WiFi congestion patterns?
- What's the relationship between thread count and network impact?
- How do different router models handle connection exhaustion?
- What are the early warning signs of network saturation?
- How effective are QoS mechanisms under stress?

---

**Remember: This tool is designed for educational research and authorized testing only. Always use responsibly and ethically.**