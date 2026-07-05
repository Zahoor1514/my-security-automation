import urllib.request
import sys

# Is baar hum real aur safe target check kar rahe hain
target_url = "https://example.com"
print(f"[+] Starting Advanced Security Headers Scan: {target_url}\n")

try:
    # Website par request bhej kar response headers nikalna
    req = urllib.request.Request(target_url, headers={'User-Agent': 'DevSecOps-Scanner-v1'})
    response = urllib.request.urlopen(req)
    headers = response.info()
    
    issues = []
    
    # 1. Check X-Frame-Options
    if 'X-Frame-Options' in headers:
        print(f"[✓] PASS: X-Frame-Options is set to ({headers['X-Frame-Options']})")
    else:
        print("[X] FAIL: X-Frame-Options is MISSING! (Risk: Clickjacking)")
        issues.append("MISSING: X-Frame-Options (High Risk of Clickjacking)")
        
    # 2. Check Content-Security-Policy
    if 'Content-Security-Policy' in headers:
        print(f"[✓] PASS: Content-Security-Policy is set.")
    else:
        print("[X] FAIL: Content-Security-Policy is MISSING! (Risk: XSS)")
        issues.append("MISSING: Content-Security-Policy (High Risk of XSS)")

    # Report Generation Logic
    if issues:
        print(f"\n[!] Scan finished. Found {len(issues)} security issues. Generating report...")
        with open("security_report.txt", "w") as report:
            report.write(f"=== SECURITY SCAN REPORT FOR {target_url} ===\n")
            for issue in issues:
                report.write(f"- {issue}\n")
        sys.exit(1) # Pipeline ko red karne ke liye taakay developer ko pata chale bugs hain
    else:
        print("\n[✓] All core security headers are present! Website is secure.")
        with open("security_report.txt", "w") as report:
            report.write(f"=== SECURITY SCAN REPORT FOR {target_url} ===\n[✓] No critical issues found.")
        sys.exit(0) # Pipeline green karne ke liye

except Exception as e:
    print(f"[X] Network Error: {e}")
    sys.exit(1)
