import urllib.request
import sys

target_url = "https://this-is-a-fake-and-dead-site-12345.com"
print(f"[+] Scanning target: {target_url}")

try:
    response = urllib.request.urlopen(target_url)
    print(f"[✓] Target is UP. Status: {response.getcode()}")
except Exception as e:
    print(f"[X] Error scanning target: {e}")
    sys.exit(1)
