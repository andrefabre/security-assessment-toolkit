# Wireshark Usage Guide for Security Assessments

## Overview
This guide covers using Wireshark for security assessments, focusing on passive network monitoring and traffic analysis. We'll cover essential features and security-focused analysis techniques.

## Installation & Setup

### 1. Installation
- Download from: https://www.wireshark.org/download.html
- Install with default options
- Install WinPcap/Npcap when prompted

### 2. Initial Configuration
1. Configure interface settings:
   - Edit > Preferences > Capture
   - Enable "Update list of packets in real time"
   - Enable "Automatically scroll during live capture"

2. Set up color rules (View > Coloring Rules):
```
Bad TCP    - tcp.analysis.flags && !tcp.analysis.window_update
Malformed  - _ws.malformed
DNS        - dns
HTTP       - http
HTTPS      - ssl || tls
```

## Basic Security Assessment Steps

### 1. Starting a Capture
1. Select correct network interface
2. Apply initial capture filter if needed:
   ```
   not broadcast and not multicast and host [target-ip]
   ```
3. Start capture (Ctrl+E)

### 2. Essential Display Filters
```
# Security-relevant filters
ssl.handshake.type == 1    # SSL/TLS Client Hello
http.authbasic             # Basic Auth (plaintext)
dns                        # DNS queries
smtp                       # Email traffic
ftp                       # FTP traffic
telnet                    # Telnet (insecure)
smb                       # Windows file sharing
ssh                       # SSH traffic

# Suspicious activity
tcp.flags.syn == 1        # SYN scans
icmp                      # Ping traffic
http.request.method == "POST" # POST requests
```

### 3. Security Analysis Features

#### Protocol Hierarchy
1. Statistics > Protocol Hierarchy
2. Look for:
   - Unencrypted protocols
   - Unusual protocols
   - High volumes of unexpected traffic

#### Endpoints Analysis
1. Statistics > Endpoints
2. Check for:
   - Unknown IP addresses
   - Suspicious ports
   - Unusual traffic patterns

#### Expert Information
1. Analyze > Expert Information
2. Focus on:
   - Errors (red)
   - Warnings (yellow)
   - Notes (blue)

## Assessment Workflows

### 1. Network Baseline Assessment
```
1. Start 5-minute capture
2. Analyze Protocol Hierarchy
3. Document normal traffic patterns
4. Identify active hosts
5. Note commonly used protocols
```

### 2. Security Issues Detection
1. Look for:
   - Cleartext passwords
   - Unencrypted protocols
   - Suspicious DNS queries
   - Port scanning activity
   - Malformed packets

### 3. SSL/TLS Analysis
1. Check encryption methods:
   ```
   ssl.handshake.ciphersuite
   ```
2. Verify certificate details:
   ```
   ssl.handshake.type == 11
   ```
3. Look for weak ciphers:
   ```
   ssl.cipher_suite == 0x0004  # TLS_RSA_WITH_RC4_128_MD5
   ```

## Evidence Collection

### 1. Packet Captures
Save relevant captures:
1. File > Save As
2. Choose format:
   - .pcapng (full detail)
   - .pcap (compatibility)

### 2. Screenshots
Capture important findings:
1. Edit > Copy > Screenshot
2. Document:
   - Suspicious traffic
   - Security issues
   - Protocol anomalies

### 3. Statistics
Export relevant statistics:
1. Statistics > Summary
2. Statistics > Protocol Hierarchy
3. Statistics > Endpoints

## Reporting Integration

### 1. Traffic Summary Template
```markdown
## Network Traffic Analysis
### Overview
- Capture Duration: [TIME]
- Total Packets: [COUNT]
- Average Rate: [RATE]

### Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

### Security Issues
- [Issue 1]
- [Issue 2]
- [Issue 3]
```

### 2. Evidence Format
```markdown
## Traffic Evidence
### Issue: [DESCRIPTION]
#### Details
- Protocol: [PROTOCOL]
- Source: [SOURCE]
- Destination: [DESTINATION]
- Time: [TIMESTAMP]

#### Impact
[SECURITY IMPACT]

#### Recommendation
[REMEDIATION STEPS]
```

## Best Practices

### 1. Capture Management
- Use ring buffer for long captures
- Filter unnecessary traffic
- Save captures regularly
- Document capture conditions

### 2. Privacy Considerations
- Avoid capturing sensitive data
- Mask personal information
- Delete unnecessary captures
- Secure stored captures

### 3. Performance Tips
- Use capture filters
- Limit capture size
- Close other applications
- Monitor system resources

## Common Issues

### 1. Capture Problems
- Check interface selection
- Verify permissions
- Confirm driver installation
- Test different interfaces

### 2. Analysis Issues
- Use appropriate filters
- Clear display filter
- Restart Wireshark
- Update software

## Integration with Assessment Tiers

### Tier 1 (Basic)
- Protocol overview
- Basic traffic patterns
- Simple security issues
- Common protocols

### Tier 2 (Enhanced)
- Detailed protocol analysis
- Security issue investigation
- Traffic pattern analysis
- Encryption verification

### Tier 3 (Comprehensive)
- Advanced protocol analysis
- Deep packet inspection
- Correlation analysis
- Custom protocol dissection

## Quick Reference

### Common Capture Filters
```
host 192.168.1.1
port 80
not broadcast
tcp port 443
```

### Essential Display Filters
```
ip.addr == 192.168.1.1
tcp.port == 80
http.request
ssl.handshake.type
```

### Keyboard Shortcuts
```
Ctrl+E   Start/Stop capture
Ctrl+R   Restart current capture
Ctrl+F   Find packet
Ctrl+B   Back to previous packet
Ctrl+N   Next packet
```

## Safety Notes
1. Only capture on authorized networks
2. Respect privacy regulations
3. Secure capture files
4. Document all activities
5. Follow assessment scope

## Additional Resources
1. Wireshark Documentation
2. Sample Captures Database
3. Protocol References
4. Security Analysis Guides

---
Note: This guide is for authorized security assessments only. Always obtain proper permissions before capturing network traffic.