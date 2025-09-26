# OSINT Tools Guide for Privacy Assessments

## Overview
This guide covers using Open Source Intelligence (OSINT) tools for privacy assessments. The focus is on identifying publicly available information that could pose security risks to individuals or organizations.

## Core OSINT Tools

### 1. theHarvester
```bash
# Installation
git clone https://github.com/laramies/theHarvester
cd theHarvester
pip3 install -r requirements.txt

# Basic Usage
python3 theHarvester.py -d [domain] -l 500 -b all

# Common Sources
-b google     # Google search
-b linkedin   # LinkedIn
-b twitter    # Twitter
-b github     # GitHub
```

### 2. Sherlock
```bash
# Installation
git clone https://github.com/sherlock-project/sherlock.git
cd sherlock
python3 -m pip install -r requirements.txt

# Usage
python3 sherlock [username]
```

### 3. Maltego (Community Edition)
- Download from: https://www.maltego.com/downloads/
- Setup guides in docs/guides/tools/maltego/

## Assessment Workflows

### 1. Personal Privacy Assessment
```bash
# Email Exposure Check
theHarvester -d [domain] -l 500 -b all > email_exposure.txt

# Social Media Presence
python3 sherlock [username] > social_media.txt

# Document Metadata
exiftool [document] > metadata.txt
```

### 2. Business Privacy Assessment
```bash
# Domain Information
whois [domain] > domain_info.txt

# Employee Exposure
theHarvester -d [domain] -b linkedin > employees.txt

# Technology Stack
whatweb [domain] > tech_stack.txt
```

### 3. Digital Footprint Analysis
```bash
# Google Dorks
site:[domain] filetype:pdf
site:[domain] inurl:admin
site:[domain] intitle:password
```

## Privacy Risk Categories

### 1. Personal Information
- Full names
- Email addresses
- Phone numbers
- Physical addresses
- Social media profiles

### 2. Professional Information
- Job titles
- Work history
- Professional networks
- Company relationships
- Project involvement

### 3. Technical Information
- IP addresses
- Domain registrations
- Technology usage
- Server information
- Email systems

## Assessment Documentation

### 1. Information Collection Template
```markdown
## Digital Exposure Report
### Basic Information
- Target: [NAME/ORGANIZATION]
- Scope: [SCOPE]
- Date: [DATE]

### Found Information
1. Personal Details
   - [DETAIL_1]
   - [DETAIL_2]

2. Professional Details
   - [DETAIL_1]
   - [DETAIL_2]

3. Technical Details
   - [DETAIL_1]
   - [DETAIL_2]
```

### 2. Risk Assessment Matrix
```markdown
| Information Type | Exposure Level | Risk Level | Mitigation |
|-----------------|----------------|------------|------------|
| Email Address   | High/Med/Low   | High       | [ACTION]   |
| Phone Number    | High/Med/Low   | Medium     | [ACTION]   |
| Home Address    | High/Med/Low   | High       | [ACTION]   |
```

## Tool-Specific Workflows

### 1. Email Investigation
```bash
# theHarvester
theHarvester -d [domain] -b all

# h8mail
h8mail -t [email]

# Email Format Check
hunter.io API search
```

### 2. Domain Investigation
```bash
# Subdomain Enumeration
sublist3r -d [domain]

# DNS Information
dnsenum [domain]

# SSL Certificate Info
sslscan [domain]
```

### 3. Social Media Investigation
```bash
# Sherlock
python3 sherlock [username]

# Social Analyzer
python3 social-analyzer --username [username]

# Twitter Analysis
twint -u [username]
```

## Privacy Protection Recommendations

### 1. Personal Privacy
```markdown
1. Information Removal
   - Google removal requests
   - Privacy policy opt-outs
   - GDPR requests

2. Account Security
   - 2FA activation
   - Strong passwords
   - Limited sharing

3. Digital Hygiene
   - Regular privacy checks
   - Content review
   - Privacy settings audit
```

### 2. Business Privacy
```markdown
1. Information Control
   - Employee guidelines
   - Data sharing policies
   - Document metadata cleaning

2. Technical Controls
   - DNS privacy
   - WHOIS privacy
   - Security headers
```

## Report Templates

### 1. Individual Assessment Report
```markdown
# Privacy Assessment Report

## Executive Summary
[Brief overview of findings]

## Digital Footprint
1. Public Profiles
2. Data Exposures
3. Security Risks

## Recommendations
1. Immediate Actions
2. Long-term Strategy
3. Monitoring Plan
```

### 2. Business Assessment Report
```markdown
# Business Privacy Assessment

## Overview
[Company digital presence]

## Exposure Analysis
1. Employee Information
2. Technical Details
3. Business Intelligence

## Risk Mitigation
1. Policy Updates
2. Technical Controls
3. Training Needs
```

## Best Practices

### 1. Assessment Ethics
- Respect privacy
- Document sources
- Legal compliance
- Ethical boundaries
- Client consent

### 2. Data Handling
- Secure storage
- Limited retention
- Clear documentation
- Secure disposal
- Access control

### 3. Client Communication
- Clear scope
- Regular updates
- Finding verification
- Action plans
- Follow-up support

## Quick Reference

### Common Commands
```bash
# Email Search
theHarvester -d [domain] -b all

# Username Search
sherlock [username]

# Domain Info
whois [domain]
dig [domain]
```

### Useful Resources
1. Privacy Laws Guide
2. OSINT Framework
3. Digital Privacy Tools
4. Removal Services

## Safety Guidelines
1. Use only legal methods
2. Respect privacy rights
3. Document all actions
4. Verify findings
5. Secure evidence

---
Note: This guide is for authorized privacy assessments only. Always obtain consent before conducting OSINT research.