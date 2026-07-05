import urllib.request
import sys
import json
import os

# 1. Dynamic Environment Variables Setup
# Agar background se variable nahi milega, to default mein example.com scan karega
TARGET_URL = os.environ.get("SCAN_TARGET", "https://example.com")
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

print(f"[+] Launching Enterprise Vulnerability Assessment Engine")
print(f"[+] Target Domain: {TARGET_URL}\n")

scan_results = {
    "target": TARGET_URL,
    "status": "Completed",
    "vulnerabilities": []
}

def send_webhook_alert(vulnerabilities):
    if not WEBHOOK_URL:
        print("[!] Webhook URL not configured in Secrets. Skipping real-time alert.")
        return
    
    # Slack Blocks Format payload formatting
    vuln_list_text = ""
    for v in vulnerabilities:
        vuln_list_text += f"• *{v['title']}* [{v['severity']}]\n"
        
    payload = {
        "text": f"🚨 *DevSecOps Pipeline Alert: Critical Violations Found!*\n"
                f"*Target Host:* {TARGET_URL}\n"
                f"*Scan Result:* FAILED ❌\n"
                f"*Detected Flaws:*\n{vuln_list_text}"
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("[✓] Real-time security alert pushed to the Operations Channel!")
    except Exception as e:
        print(f"[X] Alert Dispatch Failed: {e}")

try:
    req = urllib.request.Request(TARGET_URL, headers={'User-Agent': 'DevSecOps-Enterprise-CoreScanner-v3'})
    response = urllib.request.urlopen(req)
    headers = response.info()
    
    # === ADVANCED SECURITY HEADERS CHECKLIST ===
    
    # Rule 1: Clickjacking Protection
    if 'X-Frame-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Frame-Options Header",
            "severity": "HIGH",
            "description": "Clickjacking vulnerability. Website can be framed maliciously."
        })

    # Rule 2: XSS Mitigation
    if 'Content-Security-Policy' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing Content-Security-Policy (CSP)",
            "severity": "HIGH",
            "description": "Cross-Site Scripting mitigation controls are not defined."
        })

    # Rule 3: Content Type Sniffing Prevention
    if 'X-Content-Type-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Content-Type-Options",
            "severity": "MEDIUM",
            "description": "MIME-sniffing protection disabled. Browsers might execute non-scripts."
        })

    # Rule 4: Forced HTTPS Enforcement (HSTS)
    if 'Strict-Transport-Security' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing Strict-Transport-Security (HSTS)",
            "severity": "MEDIUM",
            "description": "Connection hijacking risk. HTTPS enforcement policy is missing."
        })

    # Rule 5: Information Leakage Check
    if 'Server' in headers and any(char.isdigit() for char in headers['Server']):
        scan_results["vulnerabilities"].append({
            "title": f"Information Leakage via Server Banner ({headers['Server']})",
            "severity": "LOW",
            "description": "Exact software versions leaked in the HTTP Response header."
        })

    # JSON Report Storage
    with open("security_report.json", "w") as report_file:
        json.dump(scan_results, report_file, indent=4)
    print("[✓] Enterprise JSON Report compiled successfully.")

    # Enforcement Logic (Fail on HIGH severity)
    high_vulnerabilities = [v for v in scan_results["vulnerabilities"] if v["severity"] == "HIGH"]
    
    if high_vulnerabilities:
        print(f"[❌] Policy Gate Blocked: {len(high_vulnerabilities)} HIGH risk vulnerabilities found!")
        send_webhook_alert(scan_results["vulnerabilities"])
        sys.exit(1)
    else:
        print("[✓] Policy Gate Passed: System architecture satisfies high-security baselines.")
        sys.exit(0)

except Exception as e:
    print(f"[X] Pipeline Execution Halted: {e}")
    sys.exit(1)
