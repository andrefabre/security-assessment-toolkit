# OWASP ZAP Usage Guide for Security Assessments

## Overview
This guide covers using OWASP Zed Attack Proxy (ZAP) for web application security testing. ZAP is a free, open-source alternative to Burp Suite, excellent for basic to intermediate web security assessments.

## Installation & Setup

### 1. Installation
- Download from: https://www.zaproxy.org/download/
- Choose appropriate package:
  - Windows: .exe installer
  - Linux: .tar.gz
  - macOS: .dmg

### 2. Initial Configuration
1. Launch ZAP
2. Complete the initial setup wizard
3. Configure browser proxy:
   - HTTP/HTTPS Proxy: 127.0.0.1:8080
   - Install ZAP root certificate

## Basic Assessment Features

### 1. Automated Scan
```
1. Enter target URL
2. Click "Automated Scan"
3. Select scan policy:
   - Basic: Quick, non-intrusive
   - Medium: Balanced
   - Full: Comprehensive
```

### 2. Manual Testing
1. Spider configuration:
   - Traditional Spider
   - Ajax Spider for JavaScript
2. Active scanning:
   - Select target
   - Choose policy
   - Start scan

### 3. Proxy Intercept
1. Enable intercept:
   - Click "Set break on all requests/responses"
2. Modify requests:
   - Headers
   - Parameters
   - Cookies

## Assessment Workflows

### Tier 1 (Basic) Assessment
```
1. Automated Scan
   - Use Basic policy
   - Spider target
   - Review alerts

2. Manual Review
   - Check SSL/TLS
   - Verify authentication
   - Review cookies
```

### Tier 2 (Enhanced) Assessment
```
1. Automated + Manual
   - Use Medium policy
   - Ajax Spider
   - Active scanning
   - Manual testing

2. Specific Tests
   - Authentication
   - Session management
   - Access control
```

### Tier 3 (Comprehensive) Assessment
```
1. Full Testing
   - Custom policies
   - Complete scanning
   - Manual verification
   - Advanced testing

2. Custom Scripts
   - Authentication
   - Session handling
   - Custom attacks
```

## Key Features

### 1. Spidering
```
Traditional Spider:
- Basic web crawling
- Form handling
- Link discovery

Ajax Spider:
- JavaScript execution
- Dynamic content
- Single-page applications
```

### 2. Active Scanning
```
Built-in Rules:
- SQL Injection
- XSS
- CSRF
- Directory traversal
- Information disclosure
```

### 3. Passive Scanning
```
Automatic Checks:
- Cookie attributes
- Header information
- Form security
- Content security
```

## Evidence Collection

### 1. Alert Documentation
```markdown
## Security Alert
### Description
[Alert description]

### Risk Level
[High/Medium/Low/Informational]

### Evidence
[Request/Response details]

### Solution
[Recommended fix]
```

### 2. Screenshots
1. Capture evidence:
   - Right-click > "Take Screenshot"
2. Document context:
   - URL
   - Steps to reproduce
   - Impact

### 3. Report Generation
1. Generate report:
   - Report > Generate Report
2. Include:
   - Executive summary
   - Technical details
   - Evidence
   - Recommendations

## Best Practices

### 1. Scanning
- Start with passive scanning
- Use appropriate scan policy
- Monitor scan progress
- Verify findings manually

### 2. Performance
- Limit scan scope
- Use context definitions
- Manage concurrent requests
- Monitor resource usage

### 3. Documentation
- Save session files
- Document configurations
- Record test cases
- Maintain evidence

## Common Issues

### 1. Connection Problems
```
Check:
- Proxy settings
- Certificate installation
- Firewall rules
- Network connectivity
```

### 2. False Positives
```
Verify:
- Manual testing
- Multiple test cases
- Different inputs
- Context consideration
```

## Integration with Reports

### 1. Finding Template
```markdown
## Web Security Finding
### Issue
[Vulnerability name]

### Description
[Detailed description]

### Evidence
[ZAP alert details]

### Impact
[Security impact]

### Remediation
[Fix recommendations]
```

### 2. Risk Rating
```
High:
- Direct security impact
- Easy exploitation
- Sensitive data exposure

Medium:
- Indirect impact
- Limited exploitation
- Partial exposure

Low:
- Minimal impact
- Difficult exploitation
- Information disclosure
```

## Safety Guidelines

### 1. Testing Scope
- Verify authorization
- Define boundaries
- Document limitations
- Monitor impact

### 2. Data Handling
- Avoid sensitive data
- Secure evidence
- Clean up after testing
- Protect reports

## Quick Reference

### Common Tasks
```
1. Start Proxy:
   Tools > Options > Local Proxies

2. Spider:
   Right-click target > Spider

3. Active Scan:
   Right-click target > Active Scan

4. Generate Report:
   Report > Generate Report
```

### Keyboard Shortcuts
```
Ctrl+B    Toggle break mode
Ctrl+E    Enable/Disable break
Ctrl+R    Go to replacer
Ctrl+H    Show history
```

## Additional Resources
1. ZAP User Guide
2. OWASP Testing Guide
3. Web Security Testing Framework
4. ZAP Weekly Releases

---
Note: Always obtain proper authorization before performing security tests on any web application.