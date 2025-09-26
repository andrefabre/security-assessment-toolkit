# Security Assessment Toolkit

A comprehensive security assessment toolkit for conducting tiered cybersecurity assessments for individuals, small businesses, and application security reviews. Includes assessment frameworks aligned with ASD Essential Eight and NIST CSF, three-tier service structure, automated security check scripts, and detailed guides.

## 🎯 Features

### Three-Tier Assessment Structure
- **Individual Tier**: Personal cybersecurity assessment for home users
- **Small Business Tier**: Organizational security assessment for SMBs
- **Application Tier**: Web application and software security reviews

### Security Frameworks
- **ASD Essential Eight**: Australian cybersecurity mitigation strategies
- **NIST Cybersecurity Framework**: Comprehensive risk management approach

### Automated Security Tools
- **Network Scanning**: Port scanning, SSL/TLS analysis, DNS security checks
- **System Hardening**: Configuration assessment, patch status, user account security
- **Packet Analysis**: Wireshark integration for network traffic analysis
- **Web Application Testing**: BurpSuite integration for vulnerability scanning

### Testing Environment
- **Vagrant/VirtualBox**: Pre-configured security testing environment
- **Tool Integration**: Seamless integration with popular security tools
- **Isolated Testing**: Safe environment for penetration testing and assessment

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/andrefabre/security-assessment-toolkit.git
   cd security-assessment-toolkit
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r config/requirements.txt
   ```

3. **Make scripts executable**
   ```bash
   chmod +x main.py
   chmod +x frameworks/*/assessment.py
   chmod +x tiers/*/assessment.py
   chmod +x scripts/*/*.py
   ```

### Basic Usage

**Run Individual Assessment**
```bash
python3 main.py --tier individual
```

**Run Small Business Assessment**
```bash
python3 main.py --tier small-business
```

**Run Application Security Assessment**
```bash
python3 main.py --tier application
```

**Run Framework Assessments**
```bash
python3 main.py --framework asd-essential-eight
python3 main.py --framework nist-csf
```

## 📊 Assessment Tiers

### Individual Tier
Personal cybersecurity assessment covering:
- Device security (computers, phones, tablets)
- Network security (Wi-Fi, router configuration)
- Password management and authentication
- Data protection and backup practices
- Online behavior and safe browsing
- Software management and updates

**Sample Usage:**
```bash
python3 main.py --tier individual
```

### Small Business Tier
Organizational security assessment including:
- Access management and user accounts
- Network security and perimeter controls
- Endpoint security and device management
- Data protection and encryption
- Incident response planning
- Security awareness training
- Vendor and third-party risk management
- Compliance and governance

**Sample Usage:**
```bash
python3 main.py --tier small-business
```

### Application Tier
Web application and software security review:
- Authentication and authorization
- Input validation and sanitization
- Data protection and encryption
- Error handling and logging
- Session management
- Configuration management
- API security
- Third-party component security
- Business logic security
- Deployment environment security

**Sample Usage:**
```bash
python3 main.py --tier application
```

## 🔍 Automated Security Scans

### Network Security Scanning
```bash
# Scan network target
python3 main.py --scan network --target 192.168.1.1

# Features:
# - Port scanning and service detection
# - SSL/TLS configuration analysis
# - HTTP security header assessment
# - DNS configuration review
# - Nmap integration (if available)
```

### System Hardening Check
```bash
# Check system security configuration
python3 main.py --scan system

# Features:
# - User account security review
# - File permission analysis  
# - Service configuration assessment
# - Network configuration review
# - System update status check
```

## 🔧 Tool Integrations

### Wireshark Integration
```bash
# Analyze packet capture file
python3 main.py --integration wireshark --pcap capture.pcap

# Features:
# - Automated security issue detection
# - Protocol analysis and statistics
# - Suspicious traffic identification
# - Network security assessment
# - Comprehensive reporting
```

### BurpSuite Integration
```bash
# Web application security scan
python3 main.py --integration burpsuite --target https://example.com

# Features:
# - Automated vulnerability scanning
# - OWASP Top 10 mapping
# - Security header analysis
# - SSL/TLS configuration testing
# - Comprehensive security reporting
```

## 🏗️ Testing Environment Setup

### Vagrant Environment
```bash
# Set up isolated testing environment
python3 main.py --setup vagrant

# Then:
cd environments/vagrant
vagrant up
vagrant ssh
```

**Pre-installed Tools:**
- Burp Suite Community Edition
- Wireshark/Tshark
- OWASP ZAP
- Nmap, Nikto, Dirb, SQLMap
- Metasploit Framework
- Various Python security libraries

**Environment Features:**
- Isolated network environment
- Pre-configured security tools
- Automated tool setup and configuration
- Easy access to assessment scripts
- Safe penetration testing sandbox

## 📋 Security Frameworks

### ASD Essential Eight
Implementation of Australian Government's Essential Eight cybersecurity strategies:

1. **Application Control** - Prevent execution of unapproved applications
2. **Patch Applications** - Update applications with security patches
3. **Configure Microsoft Office Macro Settings** - Control macro execution
4. **User Application Hardening** - Secure web browsers and PDF viewers
5. **Restrict Administrative Privileges** - Limit and monitor admin access
6. **Patch Operating Systems** - Keep OS updated with security patches
7. **Multi-factor Authentication** - Strengthen authentication mechanisms
8. **Regular Backups** - Implement and test backup procedures

**Maturity Levels:**
- ML0: Inadequate implementation
- ML1: Basic implementation
- ML2: Intermediate implementation  
- ML3: Advanced implementation

### NIST Cybersecurity Framework
Implementation of NIST CSF core functions:

1. **Identify (ID)** - Asset management, business environment, governance, risk assessment
2. **Protect (PR)** - Access control, awareness training, data security, protective technology
3. **Detect (DE)** - Anomaly detection, security monitoring, detection processes
4. **Respond (RS)** - Response planning, communications, analysis, mitigation
5. **Recover (RC)** - Recovery planning, improvements, communications

**Implementation Tiers:**
- Partial: Ad hoc, reactive approach
- Risk Informed: Risk management practices approved but not organization-wide
- Repeatable: Organization-wide approach to cybersecurity risk management
- Adaptive: Organization adapts cybersecurity practices based on lessons learned

## 📖 Documentation and Guides

### Available Guides
- [Individual Assessment Guide](guides/individual-assessment-guide.md)
- [Small Business Assessment Guide](guides/small-business-assessment-guide.md)
- [Application Security Guide](guides/application-security-assessment-guide.md)
- [ASD Essential Eight Guide](guides/asd-essential-eight-guide.md)
- [NIST CSF Guide](guides/nist-csf-guide.md)
- [Wireshark Integration Guide](guides/wireshark-integration-guide.md)
- [BurpSuite Integration Guide](guides/burpsuite-integration-guide.md)
- [Vagrant Environment Guide](guides/vagrant-environment-guide.md)

### Templates and Examples
- [Assessment Report Template](templates/assessment-report-template.md)
- Configuration examples in `config/` directory
- Sample assessment results in `examples/` directory

## 🔧 Advanced Usage

### Custom Assessments
Create custom assessment modules by extending the base assessment classes:

```python
from tiers.individual.assessment import IndividualTierAssessment

class CustomAssessment(IndividualTierAssessment):
    def __init__(self):
        super().__init__()
        # Add custom categories and questions
        self.categories["custom_category"] = {
            "name": "Custom Security Category",
            "questions": ["Custom question 1", "Custom question 2"]
        }
```

### Integration Development
Add new tool integrations by following the standard interface:

```python
class CustomToolIntegration:
    def __init__(self):
        self.results = {"tool": "Custom Tool", "findings": []}
    
    def run_scan(self, target):
        # Implement tool-specific scanning logic
        pass
    
    def generate_report(self, output_file=None):
        # Generate standardized report
        pass
```

### Configuration
Customize assessments using configuration files in the `config/` directory:

- `requirements.txt` - Python dependencies
- Custom framework configurations
- Tool-specific settings
- Report templates and formats

## 📊 Report Generation

The toolkit generates comprehensive reports in multiple formats:

### Report Types
- **Executive Summary**: High-level findings and recommendations
- **Technical Report**: Detailed findings with evidence
- **Remediation Plan**: Prioritized action items with timelines
- **Compliance Report**: Framework-specific compliance status

### Output Formats
- **Text Reports**: Human-readable assessment reports
- **JSON Data**: Structured data for further analysis
- **SARIF**: Security findings in industry-standard format
- **HTML Reports**: Web-based interactive reports (via BurpSuite)

### Sample Report Structure
```
results_20231201_143022/
├── individual_assessment_20231201_143022.txt
├── individual_results_20231201_143022.json
├── network_scan_report_192.168.1.1_20231201_143045.txt
├── wireshark_analysis_20231201_143102.txt
└── executive_summary.txt
```

## 🛡️ Security Considerations

### Safe Usage
- Only use on authorized systems and networks
- Obtain proper permissions before conducting assessments
- Follow responsible disclosure practices
- Respect privacy and data protection laws
- Use isolated environments for testing

### Legal Compliance
- Ensure compliance with local cybersecurity laws
- Obtain written authorization for penetration testing
- Follow industry-specific regulations (HIPAA, PCI-DSS, etc.)
- Document all assessment activities
- Maintain confidentiality of findings

## 🤝 Contributing

We welcome contributions to improve the Security Assessment Toolkit:

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Implement improvements or fixes
4. Add tests and documentation
5. Submit a pull request

### Areas for Contribution
- Additional assessment frameworks
- New tool integrations
- Enhanced reporting capabilities
- Documentation improvements
- Bug fixes and optimizations

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Include comprehensive documentation
- Add unit tests for new functionality
- Ensure cross-platform compatibility
- Maintain backward compatibility

## 📞 Support

### Getting Help
- Review the documentation in the `guides/` directory
- Check existing issues and discussions
- Create detailed bug reports with reproduction steps
- Follow the issue templates provided

### Community
- Share assessment experiences and best practices
- Contribute to documentation and guides
- Help other users with questions and issues
- Participate in security community discussions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This toolkit is provided for educational and authorized security testing purposes only. Users are responsible for:
- Obtaining proper authorization before use
- Complying with applicable laws and regulations
- Using the toolkit ethically and responsibly
- Maintaining confidentiality of assessment results

The authors are not responsible for any misuse or damage caused by this toolkit.

## 🏆 Acknowledgments

- Australian Signals Directorate for the Essential Eight framework
- NIST for the Cybersecurity Framework
- PortSwigger for BurpSuite integration capabilities
- Wireshark Foundation for network analysis tools
- The broader cybersecurity community for best practices and guidance
