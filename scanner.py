import urllib.request
target_url = "https://this-is-a-fake-and-dead-site-12345.com"
print(f"[+] Scanning target: {target_url}")
try:
    response = urllib.request.urlopen(target_url)
    status = response.getcode()
    print(f"[✓] Target is UP. HTTP Status Code: {status}")
except Exception as e:
    print(f"[X] Error scanning target: {e}")
    exit(1)
