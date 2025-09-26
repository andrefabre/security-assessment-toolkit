#!/usr/bin/env python3
"""
Basic Security Check Script
Performs basic security checks on a system
"""

import platform
import subprocess
import socket
import ssl
import requests
import json
from datetime import datetime

class SecurityChecker:
    def __init__(self):
        self.results = {
            'system_info': {},
            'network_info': {},
            'security_settings': {},
            'open_ports': [],
            'ssl_versions': [],
            'updates_needed': False
        }

    def check_system_info(self):
        """Gather basic system information"""
        self.results['system_info'] = {
            'os': platform.system(),
            'os_version': platform.version(),
            'machine': platform.machine(),
            'hostname': socket.gethostname()
        }

    def check_network_info(self):
        """Check basic network information"""
        hostname = socket.gethostname()
        try:
            self.results['network_info'] = {
                'hostname': hostname,
                'ip_address': socket.gethostbyname(hostname)
            }
        except socket.error as e:
            self.results['network_info'] = {
                'error': str(e)
            }

    def check_open_ports(self, ports=None):
        """Check commonly used ports"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 443, 445, 3389]
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                self.results['open_ports'].append(port)
            sock.close()

    def check_ssl_versions(self, hostname='localhost'):
        """Check supported SSL/TLS versions"""
        ssl_versions = [
            ssl.PROTOCOL_TLSv1,
            ssl.PROTOCOL_TLSv1_1,
            ssl.PROTOCOL_TLSv1_2,
            ssl.PROTOCOL_TLSv1_3
        ]
        
        for version in ssl_versions:
            try:
                context = ssl.SSLContext(version)
                with socket.create_connection((hostname, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        self.results['ssl_versions'].append(ssock.version())
            except:
                continue

    def check_updates(self):
        """Check if system updates are available"""
        if platform.system() == 'Windows':
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                   'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update\\Results\\Detect',
                                   0, winreg.KEY_READ)
                self.results['updates_needed'] = True
            except WindowsError:
                self.results['updates_needed'] = False
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(['apt-get', '-s', 'upgrade'],
                                              universal_newlines=True)
                self.results['updates_needed'] = 'upgraded' in output.lower()
            except subprocess.CalledProcessError:
                self.results['updates_needed'] = False

    def run_all_checks(self):
        """Run all security checks"""
        self.check_system_info()
        self.check_network_info()
        self.check_open_ports()
        self.check_ssl_versions()
        self.check_updates()
        return self.results

    def generate_report(self):
        """Generate a markdown report of findings"""
        report = f"""# Basic Security Assessment Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## System Information
- OS: {self.results['system_info'].get('os')}
- Version: {self.results['system_info'].get('os_version')}
- Machine: {self.results['system_info'].get('machine')}
- Hostname: {self.results['system_info'].get('hostname')}

## Network Information
- IP Address: {self.results['network_info'].get('ip_address')}

## Security Findings

### Open Ports
The following ports were found open:
{chr(10).join(['- ' + str(port) for port in self.results['open_ports']])}

### SSL/TLS Versions
Supported versions:
{chr(10).join(['- ' + str(version) for version in self.results['ssl_versions']])}

### System Updates
Updates needed: {self.results['updates_needed']}

## Recommendations
1. Review and close unnecessary open ports
2. Ensure only secure SSL/TLS versions are enabled
3. Keep system updated
"""
        return report

def main():
    checker = SecurityChecker()
    results = checker.run_all_checks()
    report = checker.generate_report()
    
    # Save results
    with open('security_check_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    with open('security_check_report.md', 'w') as f:
        f.write(report)
    
    print("Security check completed. Reports saved to:")
    print("- security_check_results.json")
    print("- security_check_report.md")

if __name__ == "__main__":
    main()