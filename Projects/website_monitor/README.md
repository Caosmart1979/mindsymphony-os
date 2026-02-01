# Website Availability Monitor

A Python-based tool for monitoring website availability and generating detailed reports.

## Features

- Check multiple websites for availability
- Measure response times
- Extract page titles
- Generate detailed reports in text format
- Save reports to timestamped files
- Error handling for various failure scenarios

## Requirements

- Python 3.x
- requests library
- beautifulsoup4 library

## Installation

The required libraries should already be installed. If not, install them using:

```bash
pip install requests beautifulsoup4
```

## Usage

### Basic Usage

Run the script with default websites:

```bash
python monitor.py
```

### Customizing the Website List

Edit the `monitor.py` file and modify the `websites` list in the `main()` function:

```python
websites = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    # Add your websites here
]
```

### Using the Monitor Class

You can also import the monitor class in your own scripts:

```python
from monitor import WebsiteMonitor

# Create monitor instance
monitor = WebsiteMonitor()

# Check websites
websites = ["https://www.google.com", "https://www.github.com"]
monitor.check_multiple_websites(websites, delay=1.0)

# Generate and print report
report = monitor.generate_report()
print(report)

# Save report to file
monitor.save_report("my_report.txt")
```

## Output

The script generates:

1. **Console Output**: Real-time progress and results
2. **Report File**: Detailed report saved as `report_YYYYMMDD_HHMMSS.txt`

### Report Format

```
================================================================================
Website Availability Report
Time: 2026-01-06 09:31:34
================================================================================

Total: 5
Accessible: 5
Inaccessible: 0
Success Rate: 100.0%

--------------------------------------------------------------------------------
Details:
--------------------------------------------------------------------------------

URL: https://www.google.com
Status: OK
Code: 200
Time: 1237.61ms
Title: Google
```

## Understanding the Results

- **Status**: 
  - `OK`: Website is accessible (HTTP 200)
  - `FAIL`: Website is not accessible
- **Code**: HTTP status code
- **Time**: Response time in milliseconds
- **Title**: Page title (if accessible)
- **Error**: Error message (if failed)

## Error Handling

The monitor handles various error scenarios:

- **Timeout**: Request took too long
- **Connection failed**: Network or DNS issues
- **HTTP errors**: Non-200 status codes
- **Other exceptions**: Unexpected errors

## Customization Options

### Adjust Timeout

Modify the timeout in `check_website()` method:

```python
result = self.check_website(url, timeout=15)  # 15 seconds
```

### Adjust Delay Between Requests

Modify the delay in `check_multiple_websites()`:

```python
monitor.check_multiple_websites(websites, delay=2.0)  # 2 seconds delay
```

### Add More Detailed Logging

Extend the `check_website()` method to capture more information:

```python
# Add response headers
result["headers"] = dict(response.headers)

# Add content length
result["content_length"] = len(response.content)
```

## Troubleshooting

### Script Runs Slowly

- Reduce the number of websites
- Decrease the delay between requests
- Adjust the timeout value

### All Websites Show as FAIL

- Check your internet connection
- Verify firewall settings
- Try accessing the websites manually

### Encoding Issues in Titles

Some websites may use special characters in titles. The script handles UTF-8 encoding, but some characters may not display correctly in all terminals.

## Advanced Usage

### Creating a Scheduled Monitor

You can use task scheduler (Windows) or cron (Linux/Mac) to run the monitor periodically:

**Windows Task Scheduler:**
```
schtasks /create /tn "Website Monitor" /tr "python C:\path\to\monitor.py" /sc daily /st 09:00
```

**Linux Cron:**
```
# Run every hour
0 * * * * /usr/bin/python3 /path/to/monitor.py
```

### Monitoring with Email Alerts

Extend the script to send email alerts when websites are down:

```python
import smtplib

def send_alert(email, website, error):
    # Add email sending logic here
    pass
```

## License

This is a free tool for educational and personal use.

## Support

For issues or questions, please check the code comments or modify the script to suit your needs.
