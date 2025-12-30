# PIN Cracker v2.0 - Authorized Penetration Testing Tool

**Created by: Shlok Sathe**  
**Repository:** https://github.com/shloksathe18-dotcom/Pin-Crack

A GUI-based PIN cracking tool designed for authorized penetration testing and security assessments. This tool helps security professionals test the strength of PIN-based authentication systems.

## ⚠️ IMPORTANT DISCLAIMER

**This tool is intended ONLY for authorized penetration testing and security research purposes. Use only on systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal and unethical.**

## Features

### 🎯 Target Configuration
- Support for multiple protocols: Telnet, SSH, HTTP Basic Auth, Custom TCP
- Configurable target IP/hostname and port
- Real-time connection testing

### 🔢 PIN Configuration
- Adjustable PIN length (1-12 digits)
- Multiple character sets:
  - Numeric only (0-9)
  - Numeric with special characters (*, #)
  - Custom character sets
- Brute force all combinations or sequential testing

### ⚡ Attack Options
- Fast mode for rapid testing
- Configurable delay between attempts
- Multi-threaded execution (up to 100 concurrent threads)
- Rate limiting to avoid detection

### 📊 Real-time Progress Dashboard
- Live progress bar and statistics
- Attempts counter and speed metrics
- Estimated time to completion (ETA)
- Current PIN being tested display

### 📝 Results Logging
- Timestamped activity log
- Color-coded status messages
- Success notifications with PIN discovery alerts

## Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/shloksathe18-dotcom/Pin-Crack.git
   cd Pin-Crack
   ```
2. Ensure Python is installed on your system
3. Run the application:
   ```bash
   python pin_craker.py
   ```

## Usage

### Basic Operation
1. **Configure Target**: Enter the target IP/hostname and port
2. **Set PIN Parameters**: Choose PIN length and character set
3. **Adjust Attack Options**: Set delay and enable fast mode if needed
4. **Start Cracking**: Click "🚀 START CRACKING" to begin
5. **Monitor Progress**: Watch real-time statistics and logs
6. **Stop if Needed**: Use "⏹️ STOP" button to halt the process

### Protocol Support
- **Telnet**: Tests common telnet PIN prompts
- **SSH**: SSH-based PIN authentication
- **HTTP Basic**: HTTP Basic authentication with PIN
- **Custom TCP**: Generic TCP socket PIN testing

### Character Sets
- `0123456789`: Standard numeric PINs
- `0123456789*`: Numeric with asterisk
- `0123456789#`: Numeric with hash
- `0123456789*#`: Numeric with both special chars
- Custom: Define your own character set

## Technical Details

### Architecture
- **GUI Framework**: tkinter with ttk styling
- **Threading**: ThreadPoolExecutor for concurrent PIN testing
- **Network**: Raw socket connections for protocol testing
- **Progress Tracking**: Real-time statistics and ETA calculation

### Success Detection
The tool identifies successful PIN attempts by looking for common success indicators:
- Shell prompts (`>`, `$`, `#`)
- Login success messages
- Root/admin prompts
- Protocol-specific success responses

### Performance
- Multi-threaded execution (configurable up to 100 threads)
- Adjustable delay between attempts (0-1000ms)
- Fast mode for maximum speed testing
- Efficient PIN generation using itertools

## Security Considerations

### Rate Limiting
- Built-in delay mechanisms to avoid triggering security systems
- Configurable timing to match target system tolerances
- Thread limiting to prevent overwhelming target systems

### Detection Avoidance
- Randomizable delays between attempts
- Connection timeout handling
- Graceful error handling to avoid system alerts

## Legal and Ethical Use

### Authorized Testing Only
- Only use on systems you own or have explicit permission to test
- Obtain proper authorization documentation before testing
- Follow responsible disclosure practices for any vulnerabilities found

### Documentation
- Keep detailed logs of all testing activities
- Document findings for security reports
- Maintain evidence of authorization for all tests

## Troubleshooting

### Common Issues
- **Connection Refused**: Check target IP/port and network connectivity
- **Slow Performance**: Adjust thread count and delay settings
- **False Positives**: Review success detection patterns for your target

### Performance Tuning
- Increase threads for faster testing (up to 100)
- Enable fast mode for maximum speed
- Adjust delay based on target system response time

## Contributing

This tool is designed for security professionals. Contributions should focus on:
- Additional protocol support
- Improved success detection
- Performance optimizations
- Security enhancements

Please submit pull requests to the main repository: https://github.com/shloksathe18-dotcom/Pin-Crack

## Author

**Shlok Sathe**  
GitHub: [@shloksathe18-dotcom](https://github.com/shloksathe18-dotcom)

## License

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations.

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally.**

*Developed by Shlok Sathe - For authorized penetration testing only*
