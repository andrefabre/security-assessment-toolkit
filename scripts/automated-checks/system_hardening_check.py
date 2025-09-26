#!/usr/bin/env python3
"""
System Hardening Check Script
Automated checks for system security hardening and configuration
"""

import os
import sys
import subprocess
import json
import platform
from datetime import datetime
from typing import Dict, List, Any


class SystemHardeningChecker:
    """System security hardening checker"""
    
    def __init__(self):
        self.results = {
            "scan_date": datetime.now().isoformat(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "checks": {}
        }
        self.os_type = platform.system().lower()
    
    def check_user_accounts(self) -> Dict[str, Any]:
        """Check user account security"""
        print("Checking user account security...")
        
        user_results = {
            "total_users": 0,
            "system_accounts": 0,
            "privileged_accounts": [],
            "password_policies": {},
            "inactive_accounts": [],
            "findings": []
        }
        
        try:
            if self.os_type == "linux":
                # Check /etc/passwd for user accounts
                with open("/etc/passwd", "r") as f:
                    users = f.readlines()
                
                user_results["total_users"] = len(users)
                
                for user_line in users:
                    parts = user_line.strip().split(":")
                    username = parts[0]
                    uid = int(parts[2])
                    shell = parts[6]
                    
                    # Check for system accounts (UID < 1000)
                    if uid < 1000:
                        user_results["system_accounts"] += 1
                    
                    # Check for privileged accounts (UID = 0)
                    if uid == 0:
                        user_results["privileged_accounts"].append(username)
                    
                    # Check for accounts with shell access
                    if "/bash" in shell or "/sh" in shell:
                        if uid >= 1000:  # Regular user with shell
                            pass  # This is normal
                        elif uid > 0:  # System account with shell
                            user_results["findings"].append(f"System account {username} has shell access")
                
                print(f"  Total users: {user_results['total_users']}")
                print(f"  System accounts: {user_results['system_accounts']}")
                print(f"  Privileged accounts: {user_results['privileged_accounts']}")
            
            elif self.os_type == "windows":
                # Windows user account checks (simplified)
                try:
                    result = subprocess.run(["net", "user"], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        # Count users (simplified parsing)
                        user_count = 0
                        for line in lines:
                            if line.strip() and not line.startswith('-') and 'User accounts' not in line:
                                user_count += len(line.split())
                        user_results["total_users"] = user_count
                        print(f"  Total users: {user_results['total_users']}")
                except:
                    user_results["findings"].append("Could not enumerate Windows users")
            
        except Exception as e:
            user_results["findings"].append(f"User account check failed: {e}")
            print(f"  Error: {e}")
        
        self.results["checks"]["user_accounts"] = user_results
        return user_results
    
    def check_file_permissions(self) -> Dict[str, Any]:
        """Check critical file permissions"""
        print("Checking file permissions...")
        
        perm_results = {
            "critical_files": {},
            "world_writable": [],
            "suid_files": [],
            "findings": []
        }
        
        try:
            if self.os_type == "linux":
                # Critical files to check
                critical_files = [
                    "/etc/passwd", "/etc/shadow", "/etc/group", "/etc/gshadow",
                    "/etc/ssh/sshd_config", "/etc/sudoers"
                ]
                
                for file_path in critical_files:
                    if os.path.exists(file_path):
                        stat_info = os.stat(file_path)
                        perms = oct(stat_info.st_mode)[-3:]
                        perm_results["critical_files"][file_path] = perms
                        
                        # Check for overly permissive permissions
                        if file_path in ["/etc/shadow", "/etc/gshadow"] and perms != "000":
                            if int(perms[1:]) > 0:  # Group or other has permissions
                                perm_results["findings"].append(f"{file_path} has overly permissive permissions: {perms}")
                        
                        print(f"  {file_path}: {perms}")
                
                # Check for world-writable files in critical directories
                critical_dirs = ["/etc", "/bin", "/sbin", "/usr/bin", "/usr/sbin"]
                for directory in critical_dirs:
                    if os.path.exists(directory):
                        try:
                            for root, dirs, files in os.walk(directory):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    try:
                                        stat_info = os.stat(file_path)
                                        if stat_info.st_mode & 0o002:  # World writable
                                            perm_results["world_writable"].append(file_path)
                                    except:
                                        continue
                                # Don't recurse too deep
                                if root.count(os.sep) - directory.count(os.sep) >= 2:
                                    dirs.clear()
                        except:
                            continue
                
                print(f"  World-writable files found: {len(perm_results['world_writable'])}")
                
        except Exception as e:
            perm_results["findings"].append(f"File permission check failed: {e}")
            print(f"  Error: {e}")
        
        self.results["checks"]["file_permissions"] = perm_results
        return perm_results
    
    def check_services(self) -> Dict[str, Any]:
        """Check running services and their security"""
        print("Checking services...")
        
        service_results = {
            "running_services": [],
            "listening_ports": [],
            "unnecessary_services": [],
            "findings": []
        }
        
        try:
            if self.os_type == "linux":
                # Check systemd services
                try:
                    result = subprocess.run(
                        ["systemctl", "list-units", "--type=service", "--state=active", "--no-pager"],
                        capture_output=True, text=True
                    )
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if '.service' in line and 'active' in line:
                                service_name = line.split()[0]
                                service_results["running_services"].append(service_name)
                        
                        print(f"  Active services: {len(service_results['running_services'])}")
                except:
                    service_results["findings"].append("Could not enumerate systemd services")
                
                # Check listening ports
                try:
                    result = subprocess.run(["netstat", "-tuln"], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if 'LISTEN' in line:
                                parts = line.split()
                                if len(parts) >= 4:
                                    service_results["listening_ports"].append(parts[3])
                        
                        print(f"  Listening ports: {len(service_results['listening_ports'])}")
                except:
                    service_results["findings"].append("Could not enumerate listening ports")
                
                # Check for potentially unnecessary services
                risky_services = [
                    "telnet", "ftp", "rsh", "rlogin", "tftp", "finger", "echo", "discard",
                    "chargen", "daytime", "time", "talk", "ntalk"
                ]
                
                for service in service_results["running_services"]:
                    service_name = service.replace('.service', '').lower()
                    if any(risky in service_name for risky in risky_services):
                        service_results["unnecessary_services"].append(service)
                        service_results["findings"].append(f"Potentially risky service running: {service}")
            
            elif self.os_type == "windows":
                # Windows service checks
                try:
                    result = subprocess.run(["sc", "query", "state=", "all"], capture_output=True, text=True)
                    if result.returncode == 0:
                        services = result.stdout.count("SERVICE_NAME:")
                        service_results["running_services"] = [f"Windows services: {services}"]
                        print(f"  Windows services found: {services}")
                except:
                    service_results["findings"].append("Could not enumerate Windows services")
                
        except Exception as e:
            service_results["findings"].append(f"Service check failed: {e}")
            print(f"  Error: {e}")
        
        self.results["checks"]["services"] = service_results
        return service_results
    
    def check_network_configuration(self) -> Dict[str, Any]:
        """Check network security configuration"""
        print("Checking network configuration...")
        
        network_results = {
            "ip_forwarding": False,
            "syn_cookies": False,
            "icmp_redirects": True,
            "source_routing": True,
            "firewall_status": "unknown",
            "findings": []
        }
        
        try:
            if self.os_type == "linux":
                # Check IP forwarding
                try:
                    with open("/proc/sys/net/ipv4/ip_forward", "r") as f:
                        ip_forward = f.read().strip()
                        network_results["ip_forwarding"] = ip_forward == "1"
                        print(f"  IP Forwarding: {network_results['ip_forwarding']}")
                        
                        if network_results["ip_forwarding"]:
                            network_results["findings"].append("IP forwarding is enabled (may be unnecessary)")
                except:
                    pass
                
                # Check SYN cookies
                try:
                    with open("/proc/sys/net/ipv4/tcp_syncookies", "r") as f:
                        syn_cookies = f.read().strip()
                        network_results["syn_cookies"] = syn_cookies == "1"
                        print(f"  SYN Cookies: {network_results['syn_cookies']}")
                        
                        if not network_results["syn_cookies"]:
                            network_results["findings"].append("SYN cookies are disabled (recommended to enable)")
                except:
                    pass
                
                # Check ICMP redirects
                try:
                    with open("/proc/sys/net/ipv4/conf/all/accept_redirects", "r") as f:
                        icmp_redirects = f.read().strip()
                        network_results["icmp_redirects"] = icmp_redirects == "1"
                        print(f"  ICMP Redirects: {network_results['icmp_redirects']}")
                        
                        if network_results["icmp_redirects"]:
                            network_results["findings"].append("ICMP redirects are enabled (security risk)")
                except:
                    pass
                
                # Check firewall status
                try:
                    # Check iptables
                    result = subprocess.run(["iptables", "-L"], capture_output=True, text=True)
                    if result.returncode == 0:
                        if "Chain INPUT (policy ACCEPT)" in result.stdout:
                            network_results["firewall_status"] = "permissive"
                            network_results["findings"].append("Firewall has permissive default policy")
                        else:
                            network_results["firewall_status"] = "configured"
                        print(f"  Firewall: {network_results['firewall_status']}")
                except:
                    try:
                        # Check ufw
                        result = subprocess.run(["ufw", "status"], capture_output=True, text=True)
                        if result.returncode == 0:
                            if "Status: active" in result.stdout:
                                network_results["firewall_status"] = "active"
                            else:
                                network_results["firewall_status"] = "inactive"
                                network_results["findings"].append("UFW firewall is inactive")
                            print(f"  UFW Firewall: {network_results['firewall_status']}")
                    except:
                        network_results["findings"].append("Could not determine firewall status")
        
        except Exception as e:
            network_results["findings"].append(f"Network configuration check failed: {e}")
            print(f"  Error: {e}")
        
        self.results["checks"]["network_configuration"] = network_results
        return network_results
    
    def check_system_updates(self) -> Dict[str, Any]:
        """Check system update status"""
        print("Checking system updates...")
        
        update_results = {
            "updates_available": 0,
            "security_updates": 0,
            "last_update": "unknown",
            "automatic_updates": False,
            "findings": []
        }
        
        try:
            if self.os_type == "linux":
                # Check for available updates (works on Debian/Ubuntu)
                try:
                    subprocess.run(["apt", "update"], capture_output=True, text=True, timeout=30)
                    result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        update_results["updates_available"] = len([l for l in lines if '/' in l]) - 1
                        
                        # Count security updates
                        security_count = 0
                        for line in lines:
                            if 'security' in line.lower():
                                security_count += 1
                        update_results["security_updates"] = security_count
                        
                        print(f"  Available updates: {update_results['updates_available']}")
                        print(f"  Security updates: {update_results['security_updates']}")
                        
                        if update_results["updates_available"] > 0:
                            update_results["findings"].append(f"{update_results['updates_available']} updates available")
                        if update_results["security_updates"] > 0:
                            update_results["findings"].append(f"{update_results['security_updates']} security updates available")
                
                except subprocess.TimeoutExpired:
                    update_results["findings"].append("Update check timed out")
                except:
                    # Try yum/dnf for Red Hat systems
                    try:
                        result = subprocess.run(["yum", "check-update"], capture_output=True, text=True)
                        if result.returncode == 100:  # Updates available
                            lines = result.stdout.split('\n')
                            update_results["updates_available"] = len([l for l in lines if l.strip() and not l.startswith('Loaded')])
                            print(f"  Available updates: {update_results['updates_available']}")
                    except:
                        update_results["findings"].append("Could not check for updates")
                
                # Check automatic updates
                if os.path.exists("/etc/apt/apt.conf.d/20auto-upgrades"):
                    try:
                        with open("/etc/apt/apt.conf.d/20auto-upgrades", "r") as f:
                            content = f.read()
                            if 'APT::Periodic::Unattended-Upgrade "1"' in content:
                                update_results["automatic_updates"] = True
                    except:
                        pass
                
                print(f"  Automatic updates: {update_results['automatic_updates']}")
                if not update_results["automatic_updates"]:
                    update_results["findings"].append("Automatic updates are not configured")
        
        except Exception as e:
            update_results["findings"].append(f"System update check failed: {e}")
            print(f"  Error: {e}")
        
        self.results["checks"]["system_updates"] = update_results
        return update_results
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate system hardening report"""
        report = f"""
System Hardening Check Report
============================

System Information:
  OS: {self.results['system']} {self.results['release']}
  Version: {self.results['version']}
  Architecture: {self.results['machine']}
  Scan Date: {self.results['scan_date']}

Security Check Results:
"""
        
        # Calculate overall security score
        total_findings = 0
        for check_name, check_results in self.results["checks"].items():
            total_findings += len(check_results.get("findings", []))
        
        if total_findings == 0:
            security_level = "Good"
        elif total_findings <= 5:
            security_level = "Fair"
        elif total_findings <= 10:
            security_level = "Poor" 
        else:
            security_level = "Critical"
        
        report += f"\nOverall Security Level: {security_level} ({total_findings} findings)\n"
        
        for check_name, check_results in self.results["checks"].items():
            report += f"\n{check_name.replace('_', ' ').title()}:\n"
            report += "-" * (len(check_name) + 1) + "\n"
            
            if check_name == "user_accounts":
                report += f"  Total Users: {check_results['total_users']}\n"
                report += f"  Privileged Accounts: {check_results['privileged_accounts']}\n"
            
            elif check_name == "services":
                report += f"  Running Services: {len(check_results['running_services'])}\n"
                report += f"  Listening Ports: {len(check_results['listening_ports'])}\n"
                report += f"  Risky Services: {len(check_results['unnecessary_services'])}\n"
            
            elif check_name == "system_updates":
                report += f"  Available Updates: {check_results['updates_available']}\n"
                report += f"  Security Updates: {check_results['security_updates']}\n"
                report += f"  Automatic Updates: {check_results['automatic_updates']}\n"
            
            # Add findings
            if check_results.get("findings"):
                report += "  Security Issues:\n"
                for finding in check_results["findings"]:
                    report += f"    - {finding}\n"
        
        report += "\nRecommendations:\n"
        report += "-" * 15 + "\n"
        report += "1. Apply all available security updates\n"
        report += "2. Configure automatic security updates\n"
        report += "3. Disable unnecessary services\n"
        report += "4. Review and restrict user privileges\n"
        report += "5. Enable and configure firewall\n"
        report += "6. Regular security monitoring and auditing\n"
        
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
    checker = SystemHardeningChecker()
    
    print("Starting system hardening check...")
    print("=" * 40)
    
    # Run security checks
    checker.check_user_accounts()
    checker.check_file_permissions()
    checker.check_services()
    checker.check_network_configuration()
    checker.check_system_updates()
    
    # Generate and save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"system_hardening_report_{timestamp}.txt"
    json_file = f"system_hardening_results_{timestamp}.json"
    
    report = checker.generate_report(report_file)
    checker.export_json(json_file)
    
    print("\n" + "="*40)
    print("SYSTEM HARDENING CHECK COMPLETE")
    print(f"Report saved to: {report_file}")
    print(f"JSON results saved to: {json_file}")


if __name__ == "__main__":
    main()