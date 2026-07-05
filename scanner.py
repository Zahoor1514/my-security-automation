import urllib.request
import sys

target_url = "https://this-is-a-fake-and-dead-site-12345.com"
print(f"[+] Scanning target: {target_url}")

try:
    response = urllib.request.urlopen(target_url)
    print(f"[✓] Target is UP.")
except Exception as e:
    error_msg = f"[X] Security Alert: Target is down or malicious. Error: {e}"
    print(error_msg)
    
    # Report File Likhna
    with open("security_report.txt", "w") as report:
        report.write(error_msg)
        
    sys.exit(1)
