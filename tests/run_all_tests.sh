#!/bin/bash
# Run All Tests Script

set -e

echo "=========================================="
echo "AI Agent Testing Framework"
echo "Running All Tests"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Run unit tests
echo -e "${YELLOW}Running Unit Tests...${NC}"
python -m pytest tests/unit/ -v --tb=short
UNIT_RESULT=$?

echo ""

# Run integration tests
echo -e "${YELLOW}Running Integration Tests...${NC}"
python -m pytest tests/integration/ -v --tb=short
INTEGRATION_RESULT=$?

echo ""

# Run performance tests
echo -e "${YELLOW}Running Performance Tests...${NC}"
python -m pytest tests/performance/ -v --tb=short -m "not slow"
PERF_RESULT=$?

echo ""

# Summary
echo "=========================================="
echo "Test Results Summary"
echo "=========================================="

if [ $UNIT_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Unit Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Unit Tests: FAILED${NC}"
fi

if [ $INTEGRATION_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Integration Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Integration Tests: FAILED${NC}"
fi

if [ $PERF_RESULT -eq 0 ]; then
    echo -e "${GREEN}✅ Performance Tests: PASSED${NC}"
else
    echo -e "${RED}❌ Performance Tests: FAILED${NC}"
fi

echo "=========================================="

# Exit with error if any test failed
if [ $UNIT_RESULT -ne 0 ] || [ $INTEGRATION_RESULT -ne 0 ] || [ $PERF_RESULT -ne 0 ]; then
    exit 1
fi

exit 0
