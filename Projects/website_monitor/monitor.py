import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import sys


class WebsiteMonitor:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def check_website(self, url, timeout=10):
        result = {"url": url, "timestamp": datetime.now().isoformat(), 
                  "accessible": False, "status_code": None, 
                  "response_time": None, "title": None, "error": None}
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
                result["url"] = url
            
            start_time = time.time()
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000
            
            result["status_code"] = response.status_code
            result["response_time"] = round(response_time, 2)
            
            if response.status_code == 200:
                result["accessible"] = True
                try:
                    soup = BeautifulSoup(response.content, "html.parser")
                    title_tag = soup.find("title")
                    if title_tag:
                        result["title"] = title_tag.get_text().strip()
                except:
                    result["title"] = "Cannot parse title"
            else:
                result["error"] = f"HTTP Status: {response.status_code}"
        except requests.exceptions.Timeout:
            result["error"] = "Timeout"
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection failed"
        except Exception as e:
            result["error"] = f"Error: {str(e)}"
        
        return result

    def check_multiple_websites(self, urls, delay=1.0):
        print(f"Checking {len(urls)} websites...")
        print()
        self.results = []
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Checking: {url}")
            result = self.check_website(url)
            self.results.append(result)
            
            status = "OK" if result["accessible"] else "FAIL"
            print(f"  Status: {status}")
            if result["status_code"]:
                print(f"  Code: {result['status_code']}")
            if result["response_time"]:
                print(f"  Time: {result['response_time']}ms")
            if result["title"]:
                print(f"  Title: {result['title']}")
            if result["error"]:
                print(f"  Error: {result['error']}")
            print()
            
            if i < len(urls):
                time.sleep(delay)
        
        return self.results

    def generate_report(self):
        if not self.results:
            return "No results"
        
        report = []
        report.append("=" * 80)
        report.append("Website Availability Report")
        report.append(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        accessible_count = sum(1 for r in self.results if r["accessible"])
        total_count = len(self.results)
        success_rate = (accessible_count / total_count * 100) if total_count > 0 else 0
        
        report.append(f"Total: {total_count}")
        report.append(f"Accessible: {accessible_count}")
        report.append(f"Inaccessible: {total_count - accessible_count}")
        report.append(f"Success Rate: {success_rate:.1f}%")
        report.append("")
        
        report.append("-" * 80)
        report.append("Details:")
        report.append("-" * 80)
        report.append("")
        
        for result in self.results:
            status = "OK" if result["accessible"] else "FAIL"
            report.append(f"URL: {result['url']}")
            report.append(f"Status: {status}")
            if result["status_code"]:
                report.append(f"Code: {result['status_code']}")
            if result["response_time"]:
                report.append(f"Time: {result['response_time']}ms")
            if result["title"]:
                report.append(f"Title: {result['title']}")
            if result["error"]:
                report.append(f"Error: {result['error']}")
            report.append("")
        
        return "\n".join(report)

    def save_report(self, filename):
        report = self.generate_report()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {filename}")


def load_websites_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            return urls
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)


def main():
    # Check if file argument is provided
    if len(sys.argv) > 1:
        if sys.argv[1] == "-f" and len(sys.argv) > 2:
            websites = load_websites_from_file(sys.argv[2])
        else:
            # Use command line arguments as URLs
            websites = sys.argv[1:]
    else:
        # Default websites
        websites = [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.python.org",
        ]
        print("No websites specified. Using default websites...")
        print()
    
    monitor = WebsiteMonitor()
    monitor.check_multiple_websites(websites, delay=1.0)
    
    print("\n" + "=" * 80)
    print("MONITORING REPORT")
    print("=" * 80)
    print()
    
    report = monitor.generate_report()
    print(report)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    monitor.save_report(f"report_{timestamp}.txt")


if __name__ == "__main__":
    main()
