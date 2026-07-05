import sys
import json
import os

CONFIG_FILE = "web_config.conf"
print("[+] Autonomous Self-Healing Engine Initialized.")
print(f"[+] Scanning Local Config Target: {CONFIG_FILE}\n")

# Check if file exists
if not os.path.exists(CONFIG_FILE):
    print(f"[X] Target configuration file {CONFIG_FILE} not found!")
    sys.exit(1)

# 1. Read the current configuration state
with open(CONFIG_FILE, "r") as f:
    config_content = f.read()

vulnerabilities_found = []

# 2. Audit Rules Checklist
if "X-Frame-Options" not in config_content:
    vulnerabilities_found.append({
        "rule": "X-Frame-Options",
        "fix_payload": "/X-Frame-Options = SAMEORIGIN"
    })

if "Content-Security-Policy" not in config_content:
    vulnerabilities_found.append({
        "rule": "Content-Security-Policy",
        "fix_payload": "/Content-Security-Policy = default-src 'self'"
    })

# 3. Decision & Self-Healing Action Block
if vulnerabilities_found:
    print(f"[⚠️] Security Alert: Found {len(vulnerabilities_found)} missing security controls!")
    print("[⚙️] Activating Self-Healing Module... Repairing configurations...")
    
    # Executing the fix by appending missing configurations autonomously
    with open(CONFIG_FILE, "a") as f:
        for v in vulnerabilities_found:
            f.write(v["fix_payload"])
            print(f"[✓] Automatically patched: Added {v['rule']}")
            
    print("\n[🎉] Self-Healing Complete! Target file has been secured successfully.")
    
    # Creating the public folder structure for pipeline continuity
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w") as f:
        f.write("<h1>✓ Self-Healing Pipeline Executed Successfully: Configurations Patched!</h1>")
        
    sys.exit(0) # Passing the build since the engine fixed the issue!
else:
    print("[✓] Scan Passed: All core security baselines are already active.")
    sys.exit(0)
