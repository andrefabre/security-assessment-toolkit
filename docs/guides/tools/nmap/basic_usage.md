# Nmap Usage Guide for Security Assessments

## Overview
This guide covers using Nmap for network discovery and security scanning during assessments. We'll focus on safe, non-intrusive scanning techniques appropriate for each assessment tier.

## Installation & Setup

### 1. Installation
- Windows: Download from https://nmap.org/download.html
- Linux: `sudo apt-get install nmap`
- Kali Linux: Pre-installed

### 2. Initial Configuration
```bash
# Create scan output directory
mkdir -p ~/security-assessments/nmap-scans
# Set up logging (add to shell profile)
export NMAP_SCAN_DIR="~/security-assessments/nmap-scans"
```

## Basic Scanning Techniques

### 1. Network Discovery (Safe Scan)
```bash
# Simple host discovery without port scanning
nmap -sn 192.168.1.0/24

# Output explanation:
# -sn: Ping Scan - disable port scan
```

### 2. Basic Port Scan
```bash
# Common ports scan
nmap -Pn -F 192.168.1.100

# Output explanation:
# -Pn: Treat all hosts as online
# -F: Fast mode - scan fewer ports
```

### 3. Service Version Detection
```bash
# Basic version detection
nmap -sV -F -T3 192.168.1.100

# Output explanation:
# -sV: Version detection
# -T3: Normal timing template
```

## Assessment Tier Integration

### Tier 1 (Basic) Scans
```bash
# Host discovery only
nmap -sn -T3 --reason [target-network]

# Basic port scan
nmap -Pn -F -T3 --open [target-ip]
```

### Tier 2 (Enhanced) Scans
```bash
# Detailed port scan
nmap -sS -sV -T3 -O [target-ip]

# Vulnerability detection
nmap -sV -sC -T3 [target-ip]
```

### Tier 3 (Comprehensive) Scans
```bash
# Full port scan with version detection
nmap -sS -sV -p- -T3 [target-ip]

# Advanced vulnerability scanning
nmap -sS -sV -sC -O -p- -T3 [target-ip]
```

## Safe Scanning Guidelines

### 1. Timing Templates
```bash
-T0  # Paranoid - Very slow, one port at a time
-T1  # Sneaky - Slow, good for IDS evasion
-T2  # Polite - Slows down to consume less bandwidth
-T3  # Normal - Default, reasonable for most scans
-T4  # Aggressive - Faster, assumes good network
-T5  # Insane - Very aggressive, likely to miss things
```

### 2. Rate Limiting
```bash
# Limit packet rate
--min-rate 100 --max-rate 500

# Limit parallel probes
--min-parallelism 10 --max-parallelism 30
```

## Output Formats

### 1. Basic Output
```bash
# Normal and XML output
nmap -sV [target] -oN scan.txt -oX scan.xml

# Output explanation:
# -oN: Normal output
# -oX: XML output
```

### 2. Structured Output
```bash
# All formats (Normal, XML, Grepable)
nmap -sV [target] -oA scan_results

# Output explanation:
# -oA: Output in all formats
```

## Evidence Collection

### 1. Standard Scan Documentation
```markdown
## Network Scan Results
### Scan Details
- Date: [DATE]
- Target: [TARGET]
- Scan Type: [SCAN_TYPE]

### Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]
```

### 2. Host Documentation
```markdown
## Host: [IP_ADDRESS]
### Open Ports
| Port | Service | Version |
|------|----------|---------|
| 80   | http     | Apache  |
| 443  | https    | nginx   |

### Security Issues
1. [Issue 1]
2. [Issue 2]
```

## Common Assessment Scripts

### 1. Basic Network Discovery
```bash
#!/bin/bash
# basic_discovery.sh
TARGET_NETWORK="$1"
OUTPUT_DIR="$NMAP_SCAN_DIR/$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"
nmap -sn -T3 "$TARGET_NETWORK" \
  -oA "$OUTPUT_DIR/discovery_scan"
```

### 2. Security Assessment Scan
```bash
#!/bin/bash
# security_scan.sh
TARGET_IP="$1"
OUTPUT_DIR="$NMAP_SCAN_DIR/$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"
nmap -sV -sC -T3 "$TARGET_IP" \
  -oA "$OUTPUT_DIR/security_scan"
```

## Best Practices

### 1. Pre-Scan Checklist
- [ ] Verify scan authorization
- [ ] Check network capacity
- [ ] Set appropriate timing
- [ ] Define clear scope
- [ ] Prepare output directory

### 2. During Scan
- Monitor network impact
- Watch for errors
- Document findings
- Adjust timing if needed
- Save incremental results

### 3. Post-Scan
- Review all outputs
- Verify scan completion
- Document anomalies
- Clean up temporary files
- Archive results securely

## Common Issues and Solutions

### 1. Scan Too Slow
```bash
# Increase timing template
nmap -T4 [target]

# Limit scope
nmap -F [target]
```

### 2. False Negatives
```bash
# Try different ping types
nmap -PS [target]  # TCP SYN Ping
nmap -PA [target]  # TCP ACK Ping
nmap -PU [target]  # UDP Ping
```

### 3. Access Denied
```bash
# Run with appropriate permissions
sudo nmap [target]

# Use less intrusive options
nmap -sT [target]  # TCP Connect Scan
```

## Safety Considerations

1. Always obtain authorization
2. Start with safe options
3. Monitor network impact
4. Document all activities
5. Secure scan results

## Quick Reference

### Common Options
```bash
-sn  # Ping scan only
-F   # Fast scan
-sV  # Version detection
-sC  # Default scripts
-O   # OS detection
-T3  # Normal timing
-Pn  # No ping
```

### Output Options
```bash
-oN  # Normal output
-oX  # XML output
-oG  # Grepable output
-oA  # All formats
```

## Integration with Other Tools

### 1. Wireshark Integration
```bash
# Capture traffic during scan
wireshark -i [interface] -k &
nmap [target]
```

### 2. Report Generation
```bash
# XML to HTML report
xsltproc scan.xml -o report.html
```

## Additional Resources
1. Nmap Documentation
2. Nmap Scripts Database
3. Security Scanning Guidelines
4. Network Discovery Best Practices

---
Note: Always ensure you have proper authorization before performing any network scans.