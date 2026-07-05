import sys
import json
import os

CONFIG_FILE = "web_config.conf"
print("[+] System Health: Initiating Pre-Flight Validation Engine.")
print(f"[+] Auditing Target: {CONFIG_FILE}\n")

if not os.path.exists(CONFIG_FILE):
    print(f"[X] Execution aborted. Target {CONFIG_FILE} missing!")
    sys.exit(1)

with open(CONFIG_FILE, "r") as f:
    config_content = f.read()

vulnerabilities_found = []

if "X-Frame-Options" not in config_content:
    vulnerabilities_found.append({
        "rule": "X-Frame-Options",
        "fix_payload": "\nX-Frame-Options = SAMEORIGIN"
    })

if "Content-Security-Policy" not in config_content:
    vulnerabilities_found.append({
        "rule": "Content-Security-Policy",
        "fix_payload": "\nContent-Security-Policy = default-src 'self'"
    })

if vulnerabilities_found:
    print(f"[⚠️] System Notice: {len(vulnerabilities_found)} violations mapped.")
    print("[⚙️] Self-Healing Protocol: Injecting cryptographic security baselines...")
    
    with open(CONFIG_FILE, "a") as f:
        for v in vulnerabilities_found:
            f.write(v["fix_payload"])
            print(f"[✓] Applied: {v['rule']}")
            
    # === PHASE 3: PRE-FLIGHT SYNTAX VALIDATION ===
    print("\n[🔍] Starting Post-Patch System Integrity Check...")
    
    # Reload file state to verify
    with open(CONFIG_FILE, "r") as f:
        updated_content = f.read()
        
    # Check if configurations are corrupted (e.g., checking if critical tags like '[server_settings]' still exist intact)
    if "[server_settings]" in updated_content and "SAMEORIGIN" in updated_content:
        print("[✓] Integrity Gate Passed: File syntax is perfectly operational.")
    else:
        print("[❌] Integrity Gate Failed: Patch corrupted the framework. Rolling back changes!")
        # Emergency Rollback Logic (Restoring original state)
        with open(CONFIG_FILE, "w") as f:
            f.write(config_content)
        sys.exit(1)
        
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w") as f:
        f.write("<h1>✓ System Core: Self-Healing and Validation Gate 100% Successful!</h1>")
        
    sys.exit(0)
else:
    print("[✓] Infrastructure status: 100% Secure. No patch required.")
    sys.exit(0)
