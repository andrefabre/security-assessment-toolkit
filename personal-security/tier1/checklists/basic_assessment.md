# Tier 1 Basic Security Assessment Checklist

## Network Security Assessment

### 1. Network Discovery
- [ ] Identify all connected devices using:
  - Network scanner (nmap)
  - Router admin panel review
  - Wireshark passive monitoring
- [ ] Document unknown devices
- [ ] Verify wireless security settings

### 2. Basic Security Checks
- [ ] Check WiFi encryption (WPA2/WPA3)
- [ ] Verify guest network separation
- [ ] Review firewall settings
- [ ] Check for default passwords

### 3. Device Security
- [ ] Operating system updates
- [ ] Antivirus status
- [ ] Backup systems
- [ ] Password policies

## Tools Required
1. Wireshark
   - Purpose: Network traffic analysis
   - Usage: Passive monitoring only
   - Duration: 5-minute capture

2. Nmap
   - Purpose: Network device discovery
   - Usage: Basic scan only (-sn option)
   - Scope: Local network only

## Assessment Steps

### 1. Initial Setup
1. Connect to client network
2. Document network details:
   - IP range
   - Gateway address
   - DNS servers

### 2. Network Analysis
1. Run Wireshark capture:
```bash
sudo python3 scripts/network/capture_utility.py -i eth0 -d 300
```

2. Run network discovery:
```bash
nmap -sn 192.168.1.0/24
```

### 3. Documentation
- Record all findings in the provided template
- Take screenshots of critical issues
- Document recommendations

## Report Generation
- Use template: templates/reports/tier1_report.md
- Include:
  - Executive summary
  - Findings
  - Recommendations
  - Next steps

## Deliverables
1. Network map
2. Device inventory
3. Security findings
4. Basic recommendations
5. Upgrade path to Tier 2

## Time Allocation
- Setup: 15 minutes
- Scanning: 30 minutes
- Analysis: 30 minutes
- Documentation: 45 minutes
- Total: 2 hours

## Notes
- This is a non-intrusive assessment
- Focus on quick wins and basic security
- Recommend Tier 2 for detailed analysis
- Document all client communications