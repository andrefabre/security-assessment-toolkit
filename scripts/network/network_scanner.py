#!/usr/bin/env python3
"""
Network Security Scanner
A basic security scanner that performs common network security checks.
"""

import argparse
import socket
import ssl
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from typing import List, Dict, Any, Tuple
import json

class SecurityScanner:
    def __init__(self, target: str, ports: List[int] = None, threads: int = 10):
        """
        Initialize the security scanner.
        
        Args:
            target: Target hostname or IP address
            ports: List of ports to scan
            threads: Number of threads to use for scanning
        """
        self.target = target
        self.ports = ports or list(range(1, 1001))  # Default: scan first 1000 ports
        self.threads = threads
        self.results: Dict[str, Any] = {
            "target": target,
            "scan_time": datetime.now().isoformat(),
            "port_scan": {},
            "ssl_scan": {},
            "http_headers": {},
            "vulnerabilities": []
        }

    def scan_port(self, port: int) -> Tuple[int, bool, str]:
        """
        Scan a single port.
        
        Args:
            port: Port number to scan
            
        Returns:
            Tuple containing (port, is_open, service_banner)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                    
                # Try to get banner
                try:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode().strip()
                except:
                    banner = ""
                
                sock.close()
                return port, True, f"{service} {banner}".strip()
            
            sock.close()
            return port, False, ""
            
        except Exception as e:
            return port, False, str(e)

    def check_ssl(self, port: int = 443) -> Dict[str, Any]:
        """
        Check SSL/TLS configuration.
        
        Args:
            port: Port to check SSL on (default: 443)
            
        Returns:
            Dictionary containing SSL information
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    return {
                        "valid": True,
                        "version": version,
                        "cipher": cipher,
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "subject": dict(x[0] for x in cert['subject']),
                        "expires": cert['notAfter']
                    }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }

    def check_http_security(self, port: int = 80) -> Dict[str, Any]:
        """
        Check HTTP security headers.
        
        Args:
            port: Port to check HTTP on (default: 80)
            
        Returns:
            Dictionary containing HTTP security information
        """
        try:
            protocols = ['http', 'https']
            results = {}
            
            for protocol in protocols:
                url = f"{protocol}://{self.target}:{port}"
                try:
                    response = requests.get(url, timeout=5, verify=False)
                    headers = response.headers
                    
                    security_headers = {
                        'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not Set'),
                        'X-Frame-Options': headers.get('X-Frame-Options', 'Not Set'),
                        'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not Set'),
                        'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not Set'),
                        'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not Set'),
                        'Server': headers.get('Server', 'Not Set')
                    }
                    
                    results[protocol] = {
                        'status_code': response.status_code,
                        'security_headers': security_headers
                    }
                except requests.exceptions.RequestException:
                    continue
                    
            return results
            
        except Exception as e:
            return {"error": str(e)}

    def scan(self) -> Dict[str, Any]:
        """
        Perform the security scan.
        
        Returns:
            Dictionary containing all scan results
        """
        # Port scanning
        print(f"[*] Starting port scan of {self.target}")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            port_results = list(executor.map(self.scan_port, self.ports))
            
        for port, is_open, banner in port_results:
            if is_open:
                self.results["port_scan"][port] = {
                    "state": "open",
                    "service": banner
                }
                
        # SSL checking for open ports
        print("[*] Checking SSL/TLS configuration")
        for port in self.results["port_scan"].keys():
            ssl_result = self.check_ssl(port)
            if ssl_result["valid"]:
                self.results["ssl_scan"][port] = ssl_result
                
        # HTTP security headers
        print("[*] Checking HTTP security headers")
        for port in self.results["port_scan"].keys():
            http_result = self.check_http_security(port)
            if http_result:
                self.results["http_headers"][port] = http_result
                
        # Basic vulnerability checks
        self.check_vulnerabilities()
                
        return self.results

    def check_vulnerabilities(self) -> None:
        """
        Perform basic vulnerability checks based on scan results.
        """
        # Check for common vulnerable ports
        vulnerable_ports = {
            21: "FTP - Clear text protocol",
            23: "Telnet - Clear text protocol",
            53: "DNS - Potential zone transfer",
            139: "NetBIOS - Windows networking",
            445: "SMB - Windows file sharing",
            3389: "RDP - Remote desktop"
        }
        
        for port, desc in vulnerable_ports.items():
            if port in self.results["port_scan"]:
                self.results["vulnerabilities"].append({
                    "type": "open_port",
                    "port": port,
                    "description": desc,
                    "severity": "medium"
                })
                
        # Check SSL/TLS configuration
        for port, ssl_info in self.results["ssl_scan"].items():
            if ssl_info.get("version", "").startswith(("SSL", "TLSv1.0", "TLSv1.1")):
                self.results["vulnerabilities"].append({
                    "type": "weak_crypto",
                    "port": port,
                    "description": f"Weak SSL/TLS version: {ssl_info['version']}",
                    "severity": "high"
                })
                
        # Check security headers
        for port, http_info in self.results["http_headers"].items():
            for protocol, data in http_info.items():
                headers = data.get('security_headers', {})
                if headers.get('Strict-Transport-Security') == 'Not Set':
                    self.results["vulnerabilities"].append({
                        "type": "missing_header",
                        "port": port,
                        "description": "Missing HSTS header",
                        "severity": "medium"
                    })
                if headers.get('X-Frame-Options') == 'Not Set':
                    self.results["vulnerabilities"].append({
                        "type": "missing_header",
                        "port": port,
                        "description": "Missing X-Frame-Options header",
                        "severity": "low"
                    })

def main():
    parser = argparse.ArgumentParser(description="Network Security Scanner")
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument("-p", "--ports", help="Comma-separated list of ports to scan", default="1-1000")
    parser.add_argument("-t", "--threads", help="Number of threads (default: 10)", type=int, default=10)
    parser.add_argument("-o", "--output", help="Output file for results", default="scan_results.json")
    args = parser.parse_args()

    # Parse port range
    try:
        if "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
            ports = list(range(start, end + 1))
        else:
            ports = list(map(int, args.ports.split(",")))
    except ValueError:
        print("Error: Invalid port range")
        sys.exit(1)

    # Create and run scanner
    scanner = SecurityScanner(args.target, ports, args.threads)
    results = scanner.scan()

    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[+] Scan completed. Results saved to {args.output}")
    
    # Print summary
    print("\nScan Summary:")
    print(f"Open Ports: {len(results['port_scan'])}")
    print(f"SSL/TLS Services: {len(results['ssl_scan'])}")
    print(f"HTTP Services: {len(results['http_headers'])}")
    print(f"Vulnerabilities Found: {len(results['vulnerabilities'])}")

if __name__ == "__main__":
    main()