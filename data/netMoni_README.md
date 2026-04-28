# netMoni.py - Network Packet Monitor

## Overview
`netMoni.py` is a Python script designed to monitor and capture all network packets on enabled network interfaces. It uses the `tcpdump` utility to capture packets for a duration of 10 seconds, saves them to a temporary PCAP file, and then converts the capture to human-readable text format for analysis.

## Features
- Captures all network packets on all enabled interfaces
- Runs for exactly 10 seconds
- Saves captured packet information to `output.txt`
- Uses intermediate PCAP file for reliable data handling
- Simple command-line execution

## Requirements
- **Python**: 3.x (tested with Python 3.8+)
- **tcpdump**: Pre-installed on macOS (located at `/usr/sbin/tcpdump`)
- **timeout**: GNU timeout utility (available via Homebrew on macOS)
- **Root privileges**: Required for packet capture (run with `sudo`)

## Installation
No additional installation is required beyond having Python and tcpdump. tcpdump is included by default on macOS systems. The `timeout` utility can be installed with:
```bash
brew install coreutils
```

## Usage
1. Navigate to the script directory:
   ```bash
   cd /path/to/SmartHome/data
   ```

2. Run the script with sudo privileges:
   ```bash
   sudo /path/to/python netMoni.py
   ```
   Replace `/path/to/python` with your Python executable path (e.g., `/Users/youruser/Documents/GitHub/SmartHome/venv/bin/python`)

3. The script will display:
   ```
   Monitoring all packets on all enabled network interfaces for 10 seconds
   To view the captured packets open the file output.txt
   ```

4. Check the captured packets in `output.txt`

## Output
- **output.txt**: Contains all captured packet information in tcpdump text format
- **output.pcap**: Temporary binary capture file (automatically cleaned up in future versions)
- If no packets are detected during the monitoring period, the file will be empty

## Configuration
- **Interface**: Scans all enabled network interfaces (`any`)
- **Duration**: Fixed at 10 seconds
- **Filter**: Captures all packets (no filtering applied)

## Troubleshooting
- **Permission denied**: Ensure you're running with `sudo`
- **tcpdump not found**: Verify tcpdump is installed (`which tcpdump`)
- **timeout not found**: Install coreutils (`brew install coreutils`)
- **Empty output**: This is normal if there's low network activity; try during higher traffic periods
- **Large output file**: The script handles large captures by processing output line-by-line
- **No packets captured**: This is normal if there's low network activity. Try running during higher traffic periods
- **Interface not found**: Verify the interface name using `ifconfig` or `networksetup -listallhardwareports`
- **tcpdump not found**: tcpdump should be available at `/usr/sbin/tcpdump` on macOS

## Example Output
```
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on en0, link-type EN10MB (Ethernet), snapshot length 524288 bytes
12:34:56.789012 ARP, Request who-has 192.168.1.1 tell 192.168.1.100, length 28
12:34:57.123456 ARP, Reply 192.168.1.1 is-at aa:bb:cc:dd:ee:ff, length 28
```

## Security Notes
- This script requires root privileges to capture network packets
- Only run on networks you have permission to monitor
- The captured data may contain sensitive network information

## Platform Support
- macOS (tested on macOS 12+)
- May work on Linux with interface name changes (eth0 instead of en0)

## License
This script is part of the SmartHome project. See main project LICENSE file for details.</content>
<parameter name="filePath">/Users/yuryyim/Documents/GitHub/SmartHome/data/netMoni_README.md