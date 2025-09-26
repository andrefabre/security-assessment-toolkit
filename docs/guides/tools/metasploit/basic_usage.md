# Metasploit Framework Usage Guide for Authorized Testing

## Overview
This guide covers using Metasploit Framework (MSF) for authorized penetration testing. Only use MSF with explicit permission and within defined scope.

⚠️ **WARNING**: Metasploit is a powerful tool that can cause system damage if misused. Only use in authorized testing environments.

## Installation & Setup

### 1. Installation
```bash
# Kali Linux (pre-installed)
sudo apt update
sudo apt install metasploit-framework

# Manual Installation
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod +x msfinstall
./msfinstall
```

### 2. Initial Setup
```bash
# Initialize database
msfdb init

# Start MSF console
msfconsole

# Update MSF
msfupdate
```

## Authorized Testing Workflow

### 1. Pre-Engagement
```bash
# Document scope
echo "Scope: [TARGET_IPS]" > engagement.txt
echo "Authorization: [AUTH_DOC]" >> engagement.txt

# Set up workspace
msfconsole
workspace -a [CLIENT_NAME]
```

### 2. Information Gathering
```bash
# Service enumeration
db_nmap -sV [TARGET]

# Import existing scans
db_import [NMAP_XML]
```

### 3. Safe Testing Methods
```bash
# Version scanning
use auxiliary/scanner/[SERVICE]/version

# Banner grabbing
use auxiliary/scanner/[SERVICE]/banner

# Service enumeration
use auxiliary/scanner/discovery/[TYPE]
```

## Assessment Tier Integration

### Tier 1 (Basic) - Passive Only
```bash
# Service identification
services
hosts

# Vulnerability check
vulns
```

### Tier 2 (Enhanced)
```bash
# Basic vulnerability scanning
use auxiliary/scanner/[SERVICE]/[SCANNER]
set RHOSTS [TARGET]
run
```

### Tier 3 (Comprehensive)
```bash
# Full security audit
use auxiliary/scanner/[SERVICE]/[DETAILED_SCANNER]
set RHOSTS [TARGET]
set THREADS 1
run
```

## Safety Guidelines

### 1. Pre-Check List
- [ ] Written authorization obtained
- [ ] Scope clearly defined
- [ ] Test environment isolated
- [ ] Backup systems verified
- [ ] Monitoring in place

### 2. Operation Rules
```bash
# Set global timeout
setg TIMEOUT 20

# Limit threads
setg THREADS 1

# Enable verbose logging
setg VERBOSE true
```

### 3. Documentation Requirements
```bash
# Start logging
spool /path/to/msf_audit.log

# Record session
sessions -v > session_log.txt

# Export results
db_export -f xml report.xml
```

## Evidence Collection

### 1. Session Documentation
```markdown
## Testing Session
- Date: [DATE]
- Target: [TARGET]
- Scope: [SCOPE]
- Authorization: [AUTH_REF]

### Activities
1. [ACTIVITY_1]
2. [ACTIVITY_2]
3. [ACTIVITY_3]
```

### 2. Finding Template
```markdown
## Security Finding
### Description
[ISSUE_DESCRIPTION]

### Technical Details
- Module: [MODULE_NAME]
- CVE: [CVE_ID]
- Risk: [RISK_LEVEL]

### Evidence
[EVIDENCE_DETAILS]

### Remediation
[FIX_RECOMMENDATIONS]
```

## Common Modules for Assessment

### 1. Service Discovery
```bash
# SMB Version
use auxiliary/scanner/smb/smb_version

# SSH Version
use auxiliary/scanner/ssh/ssh_version

# HTTP Version
use auxiliary/scanner/http/http_version
```

### 2. Security Checks
```bash
# SSL/TLS Check
use auxiliary/scanner/ssl/ssl_version

# Open Port Check
use auxiliary/scanner/portscan/tcp

# Service Enumeration
use auxiliary/scanner/discovery/udp_sweep
```

## Best Practices

### 1. Operation Security
- Use dedicated testing environment
- Monitor system resources
- Document all actions
- Regular status checks
- Clean up after testing

### 2. Resource Management
```bash
# Set resource limits
setg TIMEOUT 30
setg THREADS 1
setg RPORT [PORT]
```

### 3. Testing Process
1. Verify scope
2. Start with passive tests
3. Document findings
4. Regular backups
5. Clean environment

## Emergency Procedures

### 1. Session Management
```bash
# List sessions
sessions -l

# Kill session
sessions -k [ID]

# Kill all sessions
sessions -K
```

### 2. Emergency Shutdown
```bash
# Clean exit
sessions -K
exit -y

# Database backup
db_export -f xml backup.xml
```

## Reporting Integration

### 1. Data Export
```bash
# XML Export
db_export -f xml msf_results.xml

# HTML Report
db_export -f html msf_report.html
```

### 2. Evidence Format
```bash
# Module results
[MODULE_NAME]
- Finding: [DESCRIPTION]
- Impact: [IMPACT]
- Recommendation: [FIX]
```

## Quick Reference

### Common Commands
```bash
workspace     # Manage workspaces
hosts         # Show all hosts
services      # Show discovered services
vulns         # Show vulnerabilities
loot          # Show collected data
```

### Safety Commands
```bash
jobs          # Show running jobs
jobs -K       # Kill all jobs
unset RHOSTS  # Clear target
back          # Exit module
```

## Additional Resources
1. Metasploit Documentation
2. Rapid7 Knowledge Base
3. Practice Labs Setup
4. Testing Frameworks

---
⚠️ **IMPORTANT**: This guide is for authorized security testing only. Unauthorized use of Metasploit is illegal and unethical.