#!/usr/bin/env python3
"""
SSL/TLS Security Analyzer
Performs comprehensive SSL/TLS security analysis of a target host.
"""

import socket
import ssl
import sys
import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor

class SSLAnalyzer:
    def __init__(self, target: str, port: int = 443):
        """
        Initialize the SSL analyzer.
        
        Args:
            target: Target hostname
            port: Port to check (default: 443)
        """
        self.target = target
        self.port = port
        self.results: Dict[str, Any] = {
            "target": target,
            "port": port,
            "scan_time": datetime.now().isoformat(),
            "certificate": {},
            "protocols": {},
            "ciphers": {},
            "vulnerabilities": []
        }

    def check_protocol(self, protocol: ssl.TLSVersion) -> Tuple[str, bool, str]:
        """
        Check if a specific SSL/TLS protocol version is supported.
        
        Args:
            protocol: SSL/TLS protocol version to check
            
        Returns:
            Tuple of (protocol_name, is_supported, error_message)
        """
        try:
            context = ssl.SSLContext(protocol)
            with socket.create_connection((self.target, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    version = ssock.version()
                    return version, True, ""
        except ssl.SSLError as e:
            return str(protocol), False, str(e)
        except Exception as e:
            return str(protocol), False, str(e)

    def check_cipher(self, cipher: str) -> Tuple[str, bool, Dict[str, Any]]:
        """
        Check if a specific cipher suite is supported.
        
        Args:
            cipher: Cipher suite to check
            
        Returns:
            Tuple of (cipher_name, is_supported, cipher_info)
        """
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.set_ciphers(cipher)
            with socket.create_connection((self.target, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    return cipher, True, {
                        "protocol": ssock.version(),
                        "cipher": ssock.cipher()
                    }
        except ssl.SSLError:
            return cipher, False, {}
        except Exception as e:
            return cipher, False, {"error": str(e)}

    def get_certificate_info(self) -> Dict[str, Any]:
        """
        Get detailed certificate information.
        
        Returns:
            Dictionary containing certificate details
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target, self.port)) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "subject": dict(x[0] for x in cert['subject']),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "version": cert.get('version', 0),
                        "serialNumber": cert.get('serialNumber', ''),
                        "notBefore": cert['notBefore'],
                        "notAfter": cert['notAfter'],
                        "OCSP": cert.get('OCSP', []),
                        "caIssuers": cert.get('caIssuers', []),
                        "crlDistributionPoints": cert.get('crlDistributionPoints', []),
                        "subjectAltName": [x[1] for x in cert.get('subjectAltName', [])],
                    }
    
        except Exception as e:
            return {"error": str(e)}

    def analyze(self) -> Dict[str, Any]:
        """
        Perform the SSL/TLS analysis.
        
        Returns:
            Dictionary containing all analysis results
        """
        print(f"[*] Starting SSL/TLS analysis of {self.target}:{self.port}")
        
        # Check certificate
        print("[*] Analyzing certificate")
        self.results["certificate"] = self.get_certificate_info()
        
        # Check protocols
        print("[*] Checking supported protocols")
        protocols = [
            ssl.PROTOCOL_TLSv1,
            ssl.PROTOCOL_TLSv1_1,
            ssl.PROTOCOL_TLSv1_2,
            ssl.PROTOCOL_TLSv1_3
        ]
        
        for protocol in protocols:
            version, supported, error = self.check_protocol(protocol)
            self.results["protocols"][version] = {
                "supported": supported,
                "error": error
            }
            
        # Check cipher suites
        print("[*] Checking supported cipher suites")
        common_ciphers = [
            'HIGH', 'MEDIUM', 'LOW', 'NULL',
            'AES256-SHA', 'AES128-SHA',
            'DES-CBC3-SHA', 'RC4-SHA',
            'ECDHE-RSA-AES256-GCM-SHA384',
            'ECDHE-RSA-AES128-GCM-SHA256'
        ]
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            cipher_results = list(executor.map(self.check_cipher, common_ciphers))
            
        for cipher, supported, info in cipher_results:
            self.results["ciphers"][cipher] = {
                "supported": supported,
                "info": info
            }
            
        # Vulnerability assessment
        self.check_vulnerabilities()
        
        return self.results

    def check_vulnerabilities(self) -> None:
        """
        Check for common SSL/TLS vulnerabilities.
        """
        # Check for weak protocols
        weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']
        for protocol, info in self.results["protocols"].items():
            if info["supported"] and any(wp in protocol for wp in weak_protocols):
                self.results["vulnerabilities"].append({
                    "type": "weak_protocol",
                    "protocol": protocol,
                    "severity": "high",
                    "description": f"Weak protocol {protocol} is supported"
                })

        # Check for weak ciphers
        weak_ciphers = ['NULL', 'RC4', 'DES', 'MD5']
        for cipher, info in self.results["ciphers"].items():
            if info["supported"] and any(wc in cipher for wc in weak_ciphers):
                self.results["vulnerabilities"].append({
                    "type": "weak_cipher",
                    "cipher": cipher,
                    "severity": "high",
                    "description": f"Weak cipher {cipher} is supported"
                })

        # Check certificate validity
        cert_info = self.results["certificate"]
        if "error" not in cert_info:
            try:
                not_after = datetime.strptime(cert_info["notAfter"], "%b %d %H:%M:%S %Y %Z")
                if not_after < datetime.now():
                    self.results["vulnerabilities"].append({
                        "type": "expired_cert",
                        "severity": "critical",
                        "description": "SSL certificate has expired"
                    })
            except ValueError:
                pass

        # Check for missing security features
        if "OCSP" not in cert_info or not cert_info["OCSP"]:
            self.results["vulnerabilities"].append({
                "type": "missing_ocsp",
                "severity": "medium",
                "description": "OCSP stapling is not supported"
            })

def main():
    parser = argparse.ArgumentParser(description="SSL/TLS Security Analyzer")
    parser.add_argument("target", help="Target hostname")
    parser.add_argument("-p", "--port", type=int, default=443, help="Port to check (default: 443)")
    parser.add_argument("-o", "--output", help="Output file for results", default="ssl_analysis.json")
    args = parser.parse_args()

    try:
        analyzer = SSLAnalyzer(args.target, args.port)
        results = analyzer.analyze()

        # Save results
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"\n[+] Analysis completed. Results saved to {args.output}")
        
        # Print summary
        print("\nAnalysis Summary:")
        print(f"Certificate Valid: {'error' not in results['certificate']}")
        print("\nSupported Protocols:")
        for protocol, info in results["protocols"].items():
            if info["supported"]:
                print(f"- {protocol}")
        
        print("\nVulnerabilities Found:")
        for vuln in results["vulnerabilities"]:
            print(f"- {vuln['severity'].upper()}: {vuln['description']}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()