import urllib.request
import sys
import json
import os

TARGET_URL = os.environ.get("SCAN_TARGET", "https://example.com")
print(f"[+] Launching Enterprise Scan Engine for: {TARGET_URL}\n")

scan_results = {
    "target": TARGET_URL,
    "status": "Completed",
    "vulnerabilities": []
}

try:
    req = urllib.request.Request(TARGET_URL, headers={'User-Agent': 'DevSecOps-Enterprise-CoreScanner-v3'})
    response = urllib.request.urlopen(req)
    headers = response.info()
    
    # 1. Check X-Frame-Options
    if 'X-Frame-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Frame-Options Header",
            "severity": "HIGH",
            "desc": "Clickjacking protection missing. Site can be embedded in malicious iframes.",
            "fix": "Add 'X-Frame-Options: SAMEORIGIN' to web server config."
        })

    # 2. Check Content-Security-Policy
    if 'Content-Security-Policy' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing Content-Security-Policy (CSP)",
            "severity": "HIGH",
            "desc": "XSS mitigation missing. Malicious scripts can execute in user browsers.",
            "fix": "Define a strict Content-Security-Policy header."
        })

    # 3. Check X-Content-Type-Options
    if 'X-Content-Type-Options' not in headers:
        scan_results["vulnerabilities"].append({
            "title": "Missing X-Content-Type-Options",
            "severity": "MEDIUM",
            "desc": "MIME-sniffing protection disabled.",
            "fix": "Add 'X-Content-Type-Options: nosniff' header."
        })

    # Create 'public' directory for GitHub Pages deployment
    os.makedirs("public", exist_ok=True)

    # Save JSON data
    with open("public/security_report.json", "w") as f:
        json.dump(scan_results, f, indent=4)

    # Generate HTML Dashboard Report
    vuln_rows = ""
    for v in scan_results["vulnerabilities"]:
        color = "#dc2626" if v["severity"] == "HIGH" else "#d97706"
        vuln_rows += f"""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #edf2f7; padding-bottom: 10px; margin-bottom: 10px;">
                <h3 style="margin: 0; color: #1a202c;">{v["title"]}</h3>
                <span style="background: {color}; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;">{v["severity"]}</span>
            </div>
            <p style="margin: 5px 0; color: #4a5568;"><strong>Description:</strong> {v["desc"]}</p>
            <p style="margin: 5px 0; color: #2f855a; background: #f0fff4; padding: 8px; border-radius: 4px;"><strong>Remediation:</strong> {v["fix"]}</p>
        </div>
        """

    if not scan_results["vulnerabilities"]:
        vuln_rows = "<h3 style='color: #2f855a; text-align: center;'>✓ All Core Security Headers Present! Website is Secure.</h3>"

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>DevSecOps Security Dashboard</title>
    </head>
    <body style="font-family: Arial, sans-serif; background: #f7fafc; margin: 0; padding: 40px; color: #2d3748;">
        <div style="max-width: 900px; margin: 0 auto;">
            <div style="background: #1a202c; color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h1 style="margin: 0;">🛡️ Enterprise Security Scan Dashboard</h1>
                <p style="margin: 5px 0 0 0; color: #a0aec0;">Automated DevSecOps Pipeline Execution Results</p>
            </div>
            <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 30px;">
                <p style="margin: 5px 0;"><strong>Scan Target:</strong> <code>{TARGET_URL}</code></p>
                <p style="margin: 5px 0;"><strong>Total Vulnerabilities:</strong> <span style="font-weight:bold; color:#dc2626;">{len(scan_results["vulnerabilities"])} Issues</span></p>
            </div>
            <h2>Vulnerability Report</h2>
            {vuln_rows}
        </div>
    </body>
    </html>
    """

    with open("public/index.html", "w") as f:
        f.write(html_template)
    print("[✓] Web Dashboard compiled in public/index.html")

    # Policy Enforcement Block
    high_vulnerabilities = [v for v in scan_results["vulnerabilities"] if v["severity"] == "HIGH"]
    if high_vulnerabilities:
        print(f"[❌] Policy Gate Blocked: HIGH risk vulnerabilities found!")
        sys.exit(1)
    else:
        sys.exit(0)

except Exception as e:
    print(f"[X] Pipeline Halted: {e}")
    sys.exit(1)
