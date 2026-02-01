# Website Availability Monitor - Project Summary

## Overview

This is a Python-based website availability monitoring tool that checks multiple websites and generates detailed reports about their accessibility, response times, and status.

## Project Structure

```
website_monitor/
├── monitor.py              # Main monitoring script
├── websites.txt            # Example website list
├── README.md               # Full documentation
├── USAGE.md                # Quick usage guide
├── PROJECT_SUMMARY.md      # This file
└── report_*.txt            # Generated reports
```

## Files Description

### 1. monitor.py
The main monitoring script with the following features:
- Check single or multiple websites
- Measure response times
- Extract page titles
- Generate detailed reports
- Support for file-based website lists
- Command-line arguments

**Usage:**
```bash
python monitor.py                    # Use default websites
python monitor.py url1 url2          # Specify URLs
python monitor.py -f websites.txt    # Use file list
```

### 2. websites.txt
Example file containing a list of websites to monitor. One URL per line.

**Format:**
```
https://www.google.com
https://www.github.com
# Comments start with #
https://www.python.org
```

### 3. README.md
Complete documentation including:
- Features
- Installation
- Usage examples
- Customization options
- Troubleshooting
- Advanced usage

### 4. USAGE.md
Quick start guide for immediate use:
- Basic usage
- Understanding results
- Common HTTP codes
- Tips and troubleshooting

## Features

### Core Features
✓ Check website availability (HTTP status)
✓ Measure response times
✓ Extract page titles
✓ Error handling (timeout, connection errors, etc.)
✓ Generate timestamped reports
✓ Support for file-based website lists
✓ Command-line interface

### Error Detection
- Timeout detection
- Connection errors
- HTTP error codes (404, 500, etc.)
- Invalid URLs
- Network issues

## Requirements

### System Requirements
- Python 3.x
- Internet connection
- 10 MB free disk space

### Python Libraries
```
requests>=2.25.0
beautifulsoup4>=4.9.0
```

## Installation

1. Verify Python installation:
   ```bash
   python --version
   ```

2. Install required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Navigate to the project directory:
   ```bash
   cd website_monitor
   ```

4. Run the monitor:
   ```bash
   python monitor.py
   ```

## Configuration

### Modify Default Websites
Edit `monitor.py` and modify the `websites` list in the `main()` function.

### Adjust Timeout
Edit `monitor.py` and change the timeout parameter:
```python
result = self.check_website(url, timeout=15)  # 15 seconds
```

### Adjust Delay Between Checks
Modify the delay parameter:
```python
monitor.check_multiple_websites(websites, delay=2.0)  # 2 seconds
```

## Output

### Console Output
Real-time progress and results for each website check.

### Report File
Detailed report saved with timestamp:
- File format: `report_YYYYMMDD_HHMMSS.txt`
- Location: Same directory as the script
- Contains: Summary, detailed results, error messages

## Example Results

```
================================================================================
Website Availability Report
Time: 2026-01-06 09:36:07
================================================================================

Total: 10
Accessible: 7
Inaccessible: 3
Success Rate: 70.0%

--------------------------------------------------------------------------------
Details:
--------------------------------------------------------------------------------

URL: https://www.google.com
Status: OK
Code: 200
Time: 1931.25ms
Title: Google

URL: https://www.microsoft.com
Status: FAIL
Code: 403
Time: 856.39ms
Error: HTTP Status: 403
```

## Common Use Cases

### 1. Regular Monitoring
Set up a scheduled task to run the monitor periodically:
```bash
# Windows: Use Task Scheduler
# Linux/Mac: Use cron
0 * * * * /usr/bin/python3 /path/to/monitor.py -f websites.txt
```

### 2. Quick Check
Check a few websites quickly:
```bash
python monitor.py https://www.google.com https://www.github.com
```

### 3. Bulk Monitoring
Monitor many websites from a file:
```bash
python monitor.py -f my_websites.txt
```

## Troubleshooting

### Issue: All websites show as FAIL
**Solution:** Check internet connection and try accessing websites manually.

### Issue: 403 Forbidden errors
**Solution:** Some websites block automated access. This is normal behavior.

### Issue: Script runs slowly
**Solution:** Reduce the number of websites or decrease the delay between checks.

### Issue: Encoding problems in titles
**Solution:** Some websites use special characters. The script handles UTF-8 encoding.

## Technical Details

### HTTP Methods
- Uses GET requests
- Follows redirects automatically
- Custom User-Agent header

### Response Analysis
- Status code checking (200 = OK)
- Response time measurement (milliseconds)
- HTML title extraction using BeautifulSoup

### Error Handling
- Timeout handling (configurable)
- Connection error detection
- HTTP error code handling
- Exception catching and reporting

## Future Enhancements

Potential improvements:
- [ ] Email notifications for failures
- [ ] JSON output format
- [ ] HTML report generation
- [ ] Historical tracking
- [ ] Performance graphs
- [ ] Web interface
- [ ] Database storage
- [ ] REST API

## License

This is a free tool for educational and personal use.

## Author

Created as a demonstration of Python web scraping and monitoring capabilities.

## Version History

- **v1.0** (2026-01-06): Initial release
  - Basic website monitoring
  - Report generation
  - File-based website lists
  - Error handling

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Check USAGE.md for quick start guide
3. Review the code comments in monitor.py

---

**Last Updated:** 2026-01-06
**Version:** 1.0
**Status:** Production Ready
