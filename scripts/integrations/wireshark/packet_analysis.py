#!/usr/bin/env python3
"""
Wireshark Integration Script
Automated network packet analysis and security assessment
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import xml.etree.ElementTree as ET


class WiresharkAnalyzer:
    """Wireshark integration for network security analysis"""
    
    def __init__(self):
        self.results = {
            "analysis_date": datetime.now().isoformat(),
            "analyzer": "Wireshark Security Analyzer",
            "captures": {},
            "security_findings": []
        }
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if required tools are available"""
        tools = ["tshark", "dumpcap"]
        for tool in tools:
            try:
                subprocess.run([tool, "--version"], capture_output=True, check=True)
                print(f"✓ {tool} is available")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"✗ {tool} is not available. Please install Wireshark.")
                sys.exit(1)
    
    def capture_traffic(self, interface: str, duration: int = 60, output_file: str = None) -> str:
        """Capture network traffic using dumpcap"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"capture_{interface}_{timestamp}.pcap"
        
        print(f"Capturing traffic on {interface} for {duration} seconds...")
        
        try:
            # Use dumpcap for packet capture
            cmd = [
                "dumpcap",
                "-i", interface,
                "-a", f"duration:{duration}",
                "-w", output_file,
                "-q"  # Quiet mode
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 30)
            
            if result.returncode == 0:
                print(f"Capture completed: {output_file}")
                return output_file
            else:
                print(f"Capture failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Capture timed out")
            return None
        except Exception as e:
            print(f"Capture error: {e}")
            return None
    
    def analyze_pcap(self, pcap_file: str) -> Dict[str, Any]:
        """Analyze pcap file for security issues"""
        print(f"Analyzing {pcap_file}...")
        
        analysis_results = {
            "file": pcap_file,
            "statistics": {},
            "protocols": {},
            "security_issues": [],
            "suspicious_traffic": []
        }
        
        # Basic statistics
        analysis_results["statistics"] = self._get_basic_stats(pcap_file)
        
        # Protocol distribution
        analysis_results["protocols"] = self._get_protocol_stats(pcap_file)
        
        # Security analysis
        analysis_results["security_issues"] = self._detect_security_issues(pcap_file)
        
        # Suspicious traffic detection
        analysis_results["suspicious_traffic"] = self._detect_suspicious_traffic(pcap_file)
        
        self.results["captures"][pcap_file] = analysis_results
        return analysis_results
    
    def _get_basic_stats(self, pcap_file: str) -> Dict[str, Any]:
        """Get basic packet statistics"""
        stats = {
            "total_packets": 0,
            "total_bytes": 0,
            "duration": 0,
            "capture_info": {}
        }
        
        try:
            # Get capture info
            cmd = ["capinfos", "-T", pcap_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Number of packets:" in line:
                        stats["total_packets"] = int(line.split(':')[1].strip())
                    elif "File size:" in line:
                        stats["total_bytes"] = line.split(':')[1].strip()
                    elif "Capture duration:" in line:
                        stats["duration"] = line.split(':')[1].strip()
            
        except Exception as e:
            print(f"Error getting basic stats: {e}")
        
        return stats
    
    def _get_protocol_stats(self, pcap_file: str) -> Dict[str, int]:
        """Get protocol distribution statistics"""
        protocols = {}
        
        try:
            # Use tshark to get protocol hierarchy
            cmd = [
                "tshark", "-r", pcap_file,
                "-q", "-z", "io,phs"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('=') and 'frames' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            protocol = parts[0]
                            frames = int(parts[1])
                            protocols[protocol] = frames
        
        except Exception as e:
            print(f"Error getting protocol stats: {e}")
        
        return protocols
    
    def _detect_security_issues(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Detect various security issues in the capture"""
        security_issues = []
        
        # Check for unencrypted protocols
        unencrypted_protocols = self._check_unencrypted_protocols(pcap_file)
        security_issues.extend(unencrypted_protocols)
        
        # Check for suspicious DNS activity
        dns_issues = self._check_dns_security(pcap_file)
        security_issues.extend(dns_issues)
        
        # Check for potential data exfiltration
        exfiltration_issues = self._check_data_exfiltration(pcap_file)
        security_issues.extend(exfiltration_issues)
        
        # Check for malware indicators
        malware_indicators = self._check_malware_indicators(pcap_file)
        security_issues.extend(malware_indicators)
        
        return security_issues
    
    def _check_unencrypted_protocols(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Check for unencrypted protocol usage"""
        issues = []
        
        # Protocols to check for
        risky_protocols = {
            "http": "Unencrypted HTTP traffic detected",
            "ftp": "Unencrypted FTP traffic detected",
            "telnet": "Unencrypted Telnet traffic detected",
            "smtp": "Unencrypted SMTP traffic detected",
            "pop": "Unencrypted POP3 traffic detected",
            "imap": "Unencrypted IMAP traffic detected"
        }
        
        try:
            for protocol, message in risky_protocols.items():
                cmd = [
                    "tshark", "-r", pcap_file,
                    "-Y", protocol,
                    "-T", "fields",
                    "-e", "frame.number",
                    "-e", "ip.src",
                    "-e", "ip.dst"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    issues.append({
                        "type": "Unencrypted Protocol",
                        "protocol": protocol.upper(),
                        "message": message,
                        "count": len(lines),
                        "severity": "Medium"
                    })
        
        except Exception as e:
            print(f"Error checking unencrypted protocols: {e}")
        
        return issues
    
    def _check_dns_security(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Check for DNS security issues"""
        issues = []
        
        try:
            # Check for DNS queries to suspicious domains
            cmd = [
                "tshark", "-r", pcap_file,
                "-Y", "dns.flags.response == 0",
                "-T", "fields",
                "-e", "dns.qry.name"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                domains = result.stdout.strip().split('\n')
                suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.ru', '.cn']
                suspicious_patterns = ['dga-', 'malware', 'botnet', 'c2']
                
                suspicious_domains = []
                for domain in domains:
                    if domain and domain != '':
                        # Check for suspicious TLDs
                        for tld in suspicious_tlds:
                            if domain.endswith(tld):
                                suspicious_domains.append(domain)
                                break
                        
                        # Check for suspicious patterns
                        for pattern in suspicious_patterns:
                            if pattern in domain.lower():
                                suspicious_domains.append(domain)
                                break
                
                if suspicious_domains:
                    issues.append({
                        "type": "Suspicious DNS",
                        "protocol": "DNS",
                        "message": f"DNS queries to {len(set(suspicious_domains))} suspicious domains",
                        "domains": list(set(suspicious_domains))[:10],  # Limit to first 10
                        "severity": "High"
                    })
        
        except Exception as e:
            print(f"Error checking DNS security: {e}")
        
        return issues
    
    def _check_data_exfiltration(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Check for potential data exfiltration"""
        issues = []
        
        try:
            # Check for large outbound transfers
            cmd = [
                "tshark", "-r", pcap_file,
                "-q", "-z", "conv,ip"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if '<->' in line and 'bytes' in line:
                        parts = line.split()
                        if len(parts) >= 5:
                            try:
                                bytes_val = int(parts[4].replace(',', ''))
                                if bytes_val > 100000000:  # > 100MB
                                    issues.append({
                                        "type": "Large Data Transfer",
                                        "protocol": "IP",
                                        "message": f"Large data transfer detected: {bytes_val:,} bytes",
                                        "conversation": parts[0] + " " + parts[1] + " " + parts[2],
                                        "severity": "Medium"
                                    })
                            except ValueError:
                                continue
        
        except Exception as e:
            print(f"Error checking data exfiltration: {e}")
        
        return issues
    
    def _check_malware_indicators(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Check for malware indicators"""
        issues = []
        
        try:
            # Check for unusual ports
            cmd = [
                "tshark", "-r", pcap_file,
                "-T", "fields",
                "-e", "tcp.dstport",
                "-e", "udp.dstport"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                ports = result.stdout.strip().split('\n')
                suspicious_ports = ['4444', '5555', '6666', '7777', '8888', '9999', '31337']
                port_counts = {}
                
                for port in ports:
                    if port and port in suspicious_ports:
                        port_counts[port] = port_counts.get(port, 0) + 1
                
                if port_counts:
                    issues.append({
                        "type": "Suspicious Ports",
                        "protocol": "TCP/UDP",
                        "message": f"Traffic to suspicious ports detected",
                        "ports": port_counts,
                        "severity": "High"
                    })
        
        except Exception as e:
            print(f"Error checking malware indicators: {e}")
        
        return issues
    
    def _detect_suspicious_traffic(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Detect suspicious traffic patterns"""
        suspicious_traffic = []
        
        # Check for port scanning
        suspicious_traffic.extend(self._detect_port_scanning(pcap_file))
        
        # Check for DDoS patterns
        suspicious_traffic.extend(self._detect_ddos_patterns(pcap_file))
        
        return suspicious_traffic
    
    def _detect_port_scanning(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Detect port scanning activity"""
        issues = []
        
        try:
            # Look for TCP SYN packets to many different ports from same source
            cmd = [
                "tshark", "-r", pcap_file,
                "-Y", "tcp.flags.syn == 1 and tcp.flags.ack == 0",
                "-T", "fields",
                "-e", "ip.src",
                "-e", "tcp.dstport"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                src_ports = {}
                
                for line in lines:
                    if line and '\t' in line:
                        src, port = line.split('\t')
                        if src not in src_ports:
                            src_ports[src] = set()
                        src_ports[src].add(port)
                
                # Flag sources scanning many ports
                for src, ports in src_ports.items():
                    if len(ports) > 20:  # Scanning more than 20 ports
                        issues.append({
                            "type": "Port Scanning",
                            "source": src,
                            "message": f"Port scan detected from {src} to {len(ports)} ports",
                            "port_count": len(ports),
                            "severity": "High"
                        })
        
        except Exception as e:
            print(f"Error detecting port scanning: {e}")
        
        return issues
    
    def _detect_ddos_patterns(self, pcap_file: str) -> List[Dict[str, Any]]:
        """Detect DDoS attack patterns"""
        issues = []
        
        try:
            # Check for high packet rates to same destination
            cmd = [
                "tshark", "-r", pcap_file,
                "-T", "fields",
                "-e", "ip.dst",
                "-e", "frame.time_epoch"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                dst_counts = {}
                
                for line in lines:
                    if line and '\t' in line:
                        dst, timestamp = line.split('\t')
                        dst_counts[dst] = dst_counts.get(dst, 0) + 1
                
                # Flag destinations with very high packet counts
                for dst, count in dst_counts.items():
                    if count > 10000:  # More than 10k packets
                        issues.append({
                            "type": "Potential DDoS",
                            "destination": dst,
                            "message": f"High traffic volume to {dst}: {count:,} packets",
                            "packet_count": count,
                            "severity": "High"
                        })
        
        except Exception as e:
            print(f"Error detecting DDoS patterns: {e}")
        
        return issues
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate network analysis report"""
        report = f"""
Wireshark Network Security Analysis Report
=========================================

Analysis Date: {self.results['analysis_date']}
Analyzer: {self.results['analyzer']}

Capture Analysis Results:
"""
        
        for pcap_file, analysis in self.results["captures"].items():
            report += f"\nFile: {pcap_file}\n"
            report += "-" * (len(pcap_file) + 6) + "\n"
            
            # Statistics
            stats = analysis["statistics"]
            report += f"Total Packets: {stats.get('total_packets', 'N/A'):,}\n"
            report += f"File Size: {stats.get('total_bytes', 'N/A')}\n"
            report += f"Duration: {stats.get('duration', 'N/A')}\n"
            
            # Top protocols
            protocols = analysis["protocols"]
            if protocols:
                report += "\nTop Protocols:\n"
                sorted_protocols = sorted(protocols.items(), key=lambda x: x[1], reverse=True)[:5]
                for proto, count in sorted_protocols:
                    report += f"  {proto}: {count:,} packets\n"
            
            # Security issues
            if analysis["security_issues"]:
                report += "\nSecurity Issues:\n"
                for issue in analysis["security_issues"]:
                    report += f"  [{issue['severity']}] {issue['message']}\n"
            
            # Suspicious traffic
            if analysis["suspicious_traffic"]:
                report += "\nSuspicious Traffic:\n"
                for traffic in analysis["suspicious_traffic"]:
                    report += f"  [{traffic['severity']}] {traffic['message']}\n"
        
        # Overall recommendations
        report += "\nRecommendations:\n"
        report += "-" * 15 + "\n"
        report += "1. Encrypt all sensitive communications\n"
        report += "2. Monitor for unusual traffic patterns\n"
        report += "3. Implement network segmentation\n"
        report += "4. Use intrusion detection systems\n"
        report += "5. Regular network traffic analysis\n"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {output_file}")
        
        return report
    
    def export_json(self, output_file: str):
        """Export results as JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"Results exported to: {output_file}")


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python packet_analysis.py <pcap_file>")
        print("   or: python packet_analysis.py capture <interface> [duration]")
        sys.exit(1)
    
    analyzer = WiresharkAnalyzer()
    
    if sys.argv[1] == "capture":
        if len(sys.argv) < 3:
            print("Usage: python packet_analysis.py capture <interface> [duration]")
            sys.exit(1)
        
        interface = sys.argv[2]
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        
        # Capture traffic
        pcap_file = analyzer.capture_traffic(interface, duration)
        if not pcap_file:
            print("Capture failed")
            sys.exit(1)
    else:
        pcap_file = sys.argv[1]
        if not os.path.exists(pcap_file):
            print(f"File not found: {pcap_file}")
            sys.exit(1)
    
    print(f"Analyzing network traffic: {pcap_file}")
    print("=" * 50)
    
    # Analyze the capture
    analysis = analyzer.analyze_pcap(pcap_file)
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"wireshark_analysis_{timestamp}.txt"
    json_file = f"wireshark_results_{timestamp}.json"
    
    report = analyzer.generate_report(report_file)
    analyzer.export_json(json_file)
    
    print("\n" + "="*50)
    print("NETWORK ANALYSIS COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()