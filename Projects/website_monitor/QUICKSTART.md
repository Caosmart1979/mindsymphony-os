# Quick Start Guide - Website Monitor

## 5-Minute Setup

### Step 1: Verify Python (30 seconds)
```bash
python --version
# Should show: Python 3.x.x
```

### Step 2: Install Dependencies (1 minute)
```bash
pip install requests beautifulsoup4
```

### Step 3: Run Your First Check (30 seconds)
```bash
python monitor.py
```

That's it! You should see results immediately.

## Common Tasks

### Check Specific Websites
```bash
python monitor.py https://www.google.com https://www.github.com
```

### Create Your Website List
```bash
# Create my_websites.txt
echo "https://www.python.org" > my_websites.txt
echo "https://www.mozilla.org" >> my_websites.txt

# Run monitor on your list
python monitor.py -f my_websites.txt
```

### View Latest Report
```bash
# List all reports
ls -lt report_*.txt | head -1

# View latest report
cat report_*.txt | tail -20
```

## Understanding Your Results

### Good Results
```
Status: OK
Code: 200
Time: < 1000ms
```

### Warnings
```
Status: OK
Code: 200
Time: > 2000ms  (Slow but working)
```

### Problems
```
Status: FAIL
Code: 403/404/500
Error: Connection failed
```

## Next Steps

1. ✅ Run the basic monitor
2. ✅ Create your website list
3. ✅ Review the generated reports
4. ✅ Set up scheduled monitoring (optional)

## Schedule Automatic Checks

### Windows (Task Scheduler)
```bash
# Open Task Scheduler
# Create Basic Task → "Website Monitor"
# Trigger: Daily at 9:00 AM
# Action: Start program
#   Program: python
#   Arguments: C:\path\to\monitor.py -f websites.txt
```

### Linux/Mac (Cron)
```bash
# Edit crontab
crontab -e

# Add line for hourly checks
0 * * * * /usr/bin/python3 /path/to/monitor.py -f websites.txt
```

## Troubleshooting

### "Module not found" Error
```bash
pip install requests beautifulsoup4
```

### "Connection failed" for All Sites
Check your internet connection:
```bash
ping www.google.com
```

### 403 Forbidden Errors
This is normal! Some sites block automated access. The site is still accessible to humans.

## Need Help?

- 📖 Read `README.md` for full documentation
- 🚀 Read `USAGE.md` for usage examples
- 📊 Read `PROJECT_SUMMARY.md` for project overview

## Tips

💡 **Start Small**: Test with 2-3 websites first
💡 **Check Regularly**: Set up hourly or daily checks
💡 **Monitor Response Time**: Track website performance over time
💡 **Handle 403 Errors**: Some sites block bots - this is expected

---

**You're ready to go! Start monitoring your websites now.** 🚀
