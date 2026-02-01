#!/bin/bash

echo "=========================================="
echo "Website Monitor - Feature Demonstration"
echo "=========================================="
echo ""

echo "1. Checking single website..."
python monitor.py https://www.python.org
echo ""

echo "=========================================="
echo ""

echo "2. Checking multiple websites..."
python monitor.py https://www.google.com https://www.github.com
echo ""

echo "=========================================="
echo ""

echo "3. Checking websites from file..."
python monitor.py -f websites.txt
echo ""

echo "=========================================="
echo "Demonstration complete!"
echo "Check the generated report files for details."
echo "=========================================="
