# Network Protocol Analyzers Guide

## Overview
Network protocol analyzers are essential tools for understanding network traffic, identifying security issues, and troubleshooting network problems. This guide covers the most important tools and techniques for network protocol analysis.

## Core Protocol Analysis Tools

### 1. tcpdump
```bash
# Basic Capture
tcpdump -i [interface]

# Save to File
tcpdump -i [interface] -w capture.pcap

# Read from File
tcpdump -r capture.pcap

# Filter by Host
tcpdump host [ip-address]

# Filter by Port
tcpdump port [port-number]
```

### 2. tshark (Terminal Wireshark)
```bash
# Basic Capture
tshark -i [interface]

# Display Specific Fields
tshark -Y "http" -T fields -e http.host -e http.request.uri

# Protocol Hierarchy Statistics
tshark -r capture.pcap -q -z io,phs

# Extract HTTP Objects
tshark -r capture.pcap --export-objects http,./output
```

### 3. NetworkMiner
- Passive network sniffing
- OS fingerprinting
- File extraction
- Credential harvesting
- Host information gathering

## Protocol-Specific Analysis

### 1. HTTP/HTTPS Analysis
```bash
# Filter HTTP Traffic
tshark -Y "http" -T fields -e frame.time -e ip.src -e http.request.method -e http.host -e http.request.uri

# HTTPS Certificate Analysis
tshark -r capture.pcap -T fields -e x509sat.printableString -Y "x509sat"
```

### 2. DNS Analysis
```bash
# Filter DNS Queries
tshark -Y "dns" -T fields -e frame.time -e ip.src -e dns.qry.name

# DNS Response Analysis
tshark -Y "dns.flags.response == 1" -T fields -e dns.qry.name -e dns.resp.name
```

### 3. SMB/CIFS Analysis
```bash
# Monitor SMB Traffic
tshark -Y "smb || smb2" -T fields -e frame.time -e ip.src -e smb2.filename

# File Access Tracking
tshark -Y "smb2.filename" -T fields -e smb2.filename -e smb2.create.action
```

## Analysis Workflows

### 1. Basic Traffic Analysis
1. Capture Setup
   ```bash
   # Start Capture
   tcpdump -i any -w baseline.pcap
   ```

2. Traffic Overview
   ```bash
   # Protocol Distribution
   tshark -r baseline.pcap -q -z io,phs
   
   # Top Talkers
   tshark -r baseline.pcap -q -z endpoints,ip
   ```

### 2. Security Assessment
1. Suspicious Traffic Detection
   ```bash
   # Unusual Ports
   tshark -r capture.pcap -q -z endpoints,tcp
   
   # Large Packet Analysis
   tshark -r capture.pcap -Y "frame.len > 1500"
   ```

2. Malware Traffic Analysis
   ```bash
   # DNS Query Analysis
   tshark -r capture.pcap -Y "dns" -T fields -e dns.qry.name | sort | uniq -c
   
   # Connection Analysis
   tshark -r capture.pcap -q -z conv,tcp
   ```

## Analysis Documentation

### 1. Capture Documentation Template
```markdown
## Network Capture Analysis
### Basic Information
- Date: [DATE]
- Duration: [DURATION]
- Interface: [INTERFACE]
- Filter: [CAPTURE FILTER]

### Traffic Summary
1. Protocol Distribution
   - [PROTOCOL_1]: [PERCENTAGE]
   - [PROTOCOL_2]: [PERCENTAGE]

2. Notable Endpoints
   - [IP_1]: [DESCRIPTION]
   - [IP_2]: [DESCRIPTION]

3. Security Concerns
   - [ISSUE_1]
   - [ISSUE_2]
```

### 2. Protocol Analysis Matrix
```markdown
| Protocol | Normal Behavior | Suspicious Indicators | Risk Level |
|----------|----------------|----------------------|------------|
| HTTP     | [BASELINE]     | [INDICATORS]        | [RISK]     |
| DNS      | [BASELINE]     | [INDICATORS]        | [RISK]     |
| SMB      | [BASELINE]     | [INDICATORS]        | [RISK]     |
```

## Best Practices

### 1. Capture Best Practices
- Use appropriate capture filters
- Monitor disk space
- Rotate capture files
- Document capture settings
- Secure storage of captures

### 2. Analysis Best Practices
- Start with overview statistics
- Focus on anomalies
- Document findings
- Verify suspicious traffic
- Use multiple tools

### 3. Security Considerations
- Handle sensitive data appropriately
- Encrypt stored captures
- Limited retention periods
- Access control
- Chain of custody

## Quick Reference

### Common Capture Filters
```bash
# HTTP Traffic
tcp port 80

# HTTPS Traffic
tcp port 443

# DNS Traffic
udp port 53

# Exclude IP
not host [ip-address]
```

### Analysis Commands
```bash
# Traffic Overview
tshark -r capture.pcap -q -z io,phs

# Conversation Analysis
tshark -r capture.pcap -q -z conv,ip

# Protocol Fields
tshark -G fields | grep -i [protocol]
```

## Tool Integration

### 1. With Wireshark
- Use tshark for automation
- Share capture files
- Use same display filters
- Consistent analysis

### 2. With IDS/IPS
- Compare alerts
- Verify triggers
- Analyze packets
- Document findings

## Reporting Templates

### 1. Technical Analysis Report
```markdown
# Protocol Analysis Report

## Executive Summary
[Brief overview of findings]

## Technical Details
1. Traffic Analysis
2. Protocol Anomalies
3. Security Issues

## Recommendations
1. Immediate Actions
2. Monitoring Plans
3. Future Analysis
```

### 2. Security Assessment Report
```markdown
# Network Security Assessment

## Overview
[Analysis scope and methodology]

## Findings
1. Protocol Issues
2. Security Concerns
3. Performance Issues

## Mitigation Steps
1. Configuration Changes
2. Monitoring Updates
3. Security Controls
```

## Safety Guidelines
1. Respect privacy regulations
2. Handle sensitive data appropriately
3. Document all analysis steps
4. Secure analysis environment
5. Maintain tool updates

---
Note: This guide is for authorized network analysis only. Always obtain proper authorization before capturing network traffic.