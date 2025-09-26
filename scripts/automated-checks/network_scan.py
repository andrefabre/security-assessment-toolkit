#!/usr/bin/env python3
"""
Network Security Scanning Script
Automated network security checks and vulnerability scanning
"""

import subprocess
import json
import sys
import socket
import requests
from datetime import datetime
from typing import Dict, List, Any


class NetworkSecurityScanner:
    """Automated network security scanning utilities"""
    
    def __init__(self):
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "scanner": "Network Security Scanner",
            "tests": {}
        }
    
    def check_open_ports(self, target: str, ports: List[int] = None) -> Dict[str, Any]:
        """Check for open ports on target host"""
        if ports is None:
            # Common ports to check
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]
        
        print(f"Scanning ports on {target}...")
        open_ports = []
        closed_ports = []
        
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(3)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports.append(port)
                        print(f"  Port {port}: OPEN")
                    else:
                        closed_ports.append(port)
            except Exception as e:
                print(f"  Error checking port {port}: {e}")
                closed_ports.append(port)
        
        port_scan_results = {
            "target": target,
            "open_ports": open_ports,
            "closed_ports": closed_ports,
            "total_scanned": len(ports),
            "scan_time": datetime.now().isoformat()
        }
        
        self.results["tests"]["port_scan"] = port_scan_results
        return port_scan_results
    
    def check_ssl_tls(self, target: str, port: int = 443) -> Dict[str, Any]:
        """Check SSL/TLS configuration"""
        print(f"Checking SSL/TLS configuration for {target}:{port}...")
        
        ssl_results = {
            "target": f"{target}:{port}",
            "ssl_enabled": False,
            "certificate_valid": False,
            "tls_versions": [],
            "cipher_suites": [],
            "vulnerabilities": []
        }
        
        try:
            # Simple SSL check using requests
            response = requests.get(f"https://{target}:{port}", timeout=10, verify=True)
            ssl_results["ssl_enabled"] = True
            ssl_results["certificate_valid"] = True
            print(f"  SSL/TLS: ENABLED and VALID")
            
            # Check for common SSL/TLS vulnerabilities
            try:
                # Check for weak protocols (this is a simplified check)
                import ssl
                context = ssl.create_default_context()
                with socket.create_connection((target, port), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=target) as ssock:
                        ssl_results["tls_versions"].append(ssock.version())
                        ssl_results["cipher_suites"].append(ssock.cipher())
                        print(f"  TLS Version: {ssock.version()}")
                        print(f"  Cipher: {ssock.cipher()[0]}")
                        
                        # Check for weak ciphers
                        weak_ciphers = ["RC4", "DES", "3DES", "MD5"]
                        cipher_name = ssock.cipher()[0]
                        for weak in weak_ciphers:
                            if weak in cipher_name:
                                ssl_results["vulnerabilities"].append(f"Weak cipher: {cipher_name}")
                
            except Exception as e:
                print(f"  Detailed SSL check failed: {e}")
        
        except requests.exceptions.SSLError:
            ssl_results["ssl_enabled"] = True
            ssl_results["certificate_valid"] = False
            ssl_results["vulnerabilities"].append("Invalid SSL certificate")
            print(f"  SSL/TLS: ENABLED but INVALID certificate")
        
        except requests.exceptions.ConnectionError:
            print(f"  SSL/TLS: NOT AVAILABLE")
        
        except Exception as e:
            print(f"  SSL/TLS check failed: {e}")
        
        self.results["tests"]["ssl_tls_check"] = ssl_results
        return ssl_results
    
    def check_http_headers(self, target: str, port: int = 80) -> Dict[str, Any]:
        """Check HTTP security headers"""
        print(f"Checking HTTP security headers for {target}:{port}...")
        
        header_results = {
            "target": f"{target}:{port}",
            "security_headers": {},
            "missing_headers": [],
            "vulnerabilities": []
        }
        
        # Security headers to check
        security_headers = {
            "Strict-Transport-Security": "HSTS not implemented",
            "Content-Security-Policy": "CSP not implemented",
            "X-Content-Type-Options": "MIME type sniffing not prevented",
            "X-Frame-Options": "Clickjacking protection not implemented",
            "X-XSS-Protection": "XSS protection not enabled",
            "Referrer-Policy": "Referrer policy not set"
        }
        
        try:
            # Try HTTPS first, then HTTP
            for protocol in ["https", "http"]:
                try:
                    url = f"{protocol}://{target}:{port if protocol == 'http' or port != 80 else 443}"
                    response = requests.get(url, timeout=10, verify=False)
                    
                    for header, warning in security_headers.items():
                        if header in response.headers:
                            header_results["security_headers"][header] = response.headers[header]
                            print(f"  {header}: {response.headers[header]}")
                        else:
                            header_results["missing_headers"].append(header)
                            header_results["vulnerabilities"].append(warning)
                            print(f"  {header}: MISSING")
                    
                    # Check for information disclosure
                    info_headers = ["Server", "X-Powered-By", "X-AspNet-Version"]
                    for header in info_headers:
                        if header in response.headers:
                            header_results["vulnerabilities"].append(f"Information disclosure: {header}")
                            print(f"  {header}: {response.headers[header]} (INFORMATION DISCLOSURE)")
                    
                    break  # Success, no need to try other protocol
                
                except requests.exceptions.ConnectionError:
                    continue
                
        except Exception as e:
            print(f"  HTTP headers check failed: {e}")
        
        self.results["tests"]["http_headers"] = header_results
        return header_results
    
    def check_dns_configuration(self, domain: str) -> Dict[str, Any]:
        """Check DNS configuration and security"""
        print(f"Checking DNS configuration for {domain}...")
        
        dns_results = {
            "domain": domain,
            "records": {},
            "security_findings": []
        }
        
        # DNS record types to check
        record_types = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]
        
        for record_type in record_types:
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, record_type)
                dns_results["records"][record_type] = [str(rdata) for rdata in answers]
                print(f"  {record_type} records: {len(answers)} found")
            except ImportError:
                print("  DNS checks require dnspython: pip install dnspython")
                break
            except Exception:
                dns_results["records"][record_type] = []
        
        # Check for common DNS security issues
        if "TXT" in dns_results["records"]:
            spf_found = any("v=spf1" in record for record in dns_results["records"]["TXT"])
            dmarc_found = any("v=DMARC1" in record for record in dns_results["records"]["TXT"])
            
            if not spf_found:
                dns_results["security_findings"].append("SPF record not found")
            if not dmarc_found:
                dns_results["security_findings"].append("DMARC record not found")
        
        self.results["tests"]["dns_check"] = dns_results
        return dns_results
    
    def run_nmap_scan(self, target: str, scan_type: str = "basic") -> Dict[str, Any]:
        """Run nmap scan if available"""
        print(f"Running nmap scan on {target}...")
        
        nmap_results = {
            "target": target,
            "scan_type": scan_type,
            "command": "",
            "output": "",
            "available": False
        }
        
        # Define nmap commands for different scan types
        nmap_commands = {
            "basic": f"nmap -sS -O -sV -T4 {target}",
            "vuln": f"nmap -sV --script vuln {target}",
            "stealth": f"nmap -sS -T2 {target}"
        }
        
        try:
            command = nmap_commands.get(scan_type, nmap_commands["basic"])
            nmap_results["command"] = command
            
            # Check if nmap is available
            subprocess.run(["nmap", "--version"], capture_output=True, check=True)
            nmap_results["available"] = True
            
            # Run the scan
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            nmap_results["output"] = result.stdout
            print(f"  Nmap scan completed successfully")
            
        except subprocess.CalledProcessError:
            nmap_results["output"] = "Nmap not available or failed to run"
            print(f"  Nmap not available")
        except subprocess.TimeoutExpired:
            nmap_results["output"] = "Scan timed out"
            print(f"  Nmap scan timed out")
        except Exception as e:
            nmap_results["output"] = f"Error: {e}"
            print(f"  Nmap scan failed: {e}")
        
        self.results["tests"]["nmap_scan"] = nmap_results
        return nmap_results
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate network security scan report"""
        report = f"""
Network Security Scan Report
===========================

Scan Date: {self.results['scan_date']}
Scanner: {self.results['scanner']}

Test Results:
"""
        
        for test_name, test_results in self.results["tests"].items():
            report += f"\n{test_name.replace('_', ' ').title()}:\n"
            report += "-" * (len(test_name) + 1) + "\n"
            
            if test_name == "port_scan":
                report += f"Target: {test_results['target']}\n"
                report += f"Open Ports: {test_results['open_ports']}\n"
                report += f"Total Scanned: {test_results['total_scanned']}\n"
                if test_results['open_ports']:
                    report += "Security Recommendation: Review open ports and close unnecessary services\n"
            
            elif test_name == "ssl_tls_check":
                report += f"Target: {test_results['target']}\n"
                report += f"SSL Enabled: {test_results['ssl_enabled']}\n"
                report += f"Certificate Valid: {test_results['certificate_valid']}\n"
                if test_results['vulnerabilities']:
                    report += f"Vulnerabilities: {', '.join(test_results['vulnerabilities'])}\n"
            
            elif test_name == "http_headers":
                report += f"Target: {test_results['target']}\n"
                report += f"Missing Headers: {len(test_results['missing_headers'])}\n"
                if test_results['vulnerabilities']:
                    report += "Security Issues:\n"
                    for vuln in test_results['vulnerabilities']:
                        report += f"  - {vuln}\n"
        
        report += "\nRecommendations:\n"
        report += "-" * 15 + "\n"
        report += "1. Close unnecessary open ports\n"
        report += "2. Implement proper SSL/TLS configuration\n"
        report += "3. Add missing security headers\n"
        report += "4. Regular vulnerability scanning\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python network_scan.py <target>")
        print("Example: python network_scan.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = NetworkSecurityScanner()
    
    print(f"Starting network security scan for: {target}")
    print("=" * 50)
    
    # Run various security checks
    scanner.check_open_ports(target)
    scanner.check_ssl_tls(target)
    scanner.check_http_headers(target)
    scanner.check_dns_configuration(target)
    scanner.run_nmap_scan(target)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"network_scan_report_{target}_{timestamp}.txt"
    json_file = f"network_scan_results_{target}_{timestamp}.json"
    
    report = scanner.generate_report(report_file)
    scanner.export_json(json_file)
    
    print("\n" + "="*50)
    print("NETWORK SCAN COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()