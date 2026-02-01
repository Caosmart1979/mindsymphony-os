# Website Monitor - Quick Usage Guide

## Installation

1. Make sure you have Python 3.x installed
2. Install required libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

## Basic Usage

### Method 1: Use Default Websites
```bash
python monitor.py
```

### Method 2: Specify Websites Directly
```bash
python monitor.py https://www.google.com https://www.github.com
```

### Method 3: Use a File List
```bash
python monitor.py -f websites.txt
```

## Creating Your Website List

Create a file called `websites.txt` with one URL per line:
```
https://www.google.com
https://www.github.com
https://www.python.org
```

You can add comments with `#`:
```
# Search engines
https://www.google.com
https://www.bing.com

# Development
https://www.github.com
https://www.stackoverflow.com
```

## Understanding Results

The script will show:
- **Status**: OK (accessible) or FAIL (not accessible)
- **Code**: HTTP status code (200 is good)
- **Time**: Response time in milliseconds
- **Title**: Page title (if accessible)
- **Error**: Error message (if failed)

## Example Output

```
Checking 3 websites...

[1/3] Checking: https://www.google.com
  Status: OK
  Code: 200
  Time: 1234.56ms
  Title: Google

[2/3] Checking: https://www.github.com
  Status: OK
  Code: 200
  Time: 2345.67ms
  Title: GitHub: Where the world builds software

[3/3] Checking: https://www.example.com
  Status: FAIL
  Error: Connection failed
```

## Reports

Reports are automatically saved with timestamp:
- `report_20260106_123456.txt` - Text format report

## Common HTTP Status Codes

- **200**: OK - Website is working
- **403**: Forbidden - Access denied (bot protection)
- **404**: Not Found - Page doesn't exist
- **500**: Server Error - Website has problems
- **503**: Service Unavailable - Website is down

## Tips

1. **Use HTTPS**: Most websites require HTTPS
2. **Check Response Time**: Lower is better (< 1000ms = fast)
3. **Handle 403 Errors**: Some sites block automated access
4. **Adjust Delays**: The script waits 1 second between checks to avoid being blocked

## Troubleshooting

### All websites show FAIL
- Check your internet connection
- Try accessing websites manually in a browser
- Check if a firewall is blocking Python

### Some websites show 403 Forbidden
- This is normal - some sites block automated access
- The website is still accessible to humans
- Consider using different user agents or cookies

### Script runs slowly
- Reduce the number of websites in your list
- The delay between checks helps avoid being blocked

## Advanced: Scheduling

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\monitor.py -f websites.txt`

### Linux/Mac (Cron)
```bash
# Edit crontab
crontab -e

# Add this line to run every hour
0 * * * * /usr/bin/python3 /path/to/monitor.py -f websites.txt
```

## Support

For more details, see README.md
