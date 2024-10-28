import subprocess

def run_windows_defender_scan():
    command = ["powershell", "Start-MpScan", "-ScanType", "QuickScan"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Quick scan completed successfully.")
        print(result.stdout)
    else:
        print("Quick scan failed.")
        print(result.stderr)

def check_install_updates():
    try:
        print("Checking for updates...")
        subprocess.run(["usoclient", "StartScan"], check=True)
        print("Update check initiated.")
        print("Installing updates...")
        subprocess.run(["usoclient", "StartInstall"], check=True)
        print("Update installation initiated.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to check or install updates: {e}")

if __name__ == "__main__":
    run_windows_defender_scan()
    check_install_updates()
