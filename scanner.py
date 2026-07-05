import urllib.request
import sys
import json

target_url = "https://example.com"
print(f"[+] Launching Enterprise Security Scan: {target_url}\n")

# Report Structure Initialization
scan_results = {
    "target": target_url,
    "status": "Completed",
    "vulnerabilities": []
}

try:
    req = urllib.request.Request(target_url, headers={'User-Agent': 'DevSecOps-Enterprise-Scanner-v2'})
    response = urllib.request.urlopen(req)
    headers = response.info()
    
    # 1. Check X-Frame-Options (High Severity)
    if 'X-Frame-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Frame-Options Header",
            "severity": "HIGH",
            "description": "Clickjacking protection is not enforced. Attackers can embed this site in an iframe.",
            "remediation": "Add 'X-Frame-Options: DENY' or 'SAMEORIGIN' to server configuration."
        })

    # 2. Check Content-Security-Policy (High Severity)
    if 'Content-Security-Policy' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing Content-Security-Policy (CSP)",
            "severity": "HIGH",
            "description": "Cross-Site Scripting (XSS) mitigation is missing.",
            "remediation": "Define a robust CSP header to restrict script execution sources."
        })

    # 3. Check X-Content-Type-Options (Medium/Low Severity)
    if 'X-Content-Type-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Content-Type-Options",
            "severity": "MEDIUM",
            "description": "MIME-sniffing protection is disabled.",
            "remediation": "Add 'X-Content-Type-Options: nosniff' header."
        })

    # Saving Results to a Professional JSON Report
    with open("security_report.json", "w") as report_file:
        json.dump(scan_results, report_file, indent=4)
        
    print(f"[!] Scan finished. JSON report generated successfully.")

    # Rule-Based Pipeline Enforcement
    high_or_critical_found = any(v["severity"] == "HIGH" for v in scan_results["vulnerabilities"])
    
    if high_or_critical_found:
        print("[❌] Strict Policy Violation: HIGH severity vulnerabilities found. Failing build!")
        sys.exit(1)
    else:
        print("[✓] Policy Passed: No High severity vulnerabilities found.")
        sys.exit(0)

except Exception as e:
    print(f"[X] Scan Interrupted due to Network Error: {e}")
    sys.exit(1)
