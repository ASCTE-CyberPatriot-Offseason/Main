import subprocess

def manage_services():
    services_to_disable = [
        "TermService", "SharedAccess", "UmRdpService", "ftpsvc",
        "RemoteRegistry", "SessionEnv", "SSDPSRV", "upnphost", "W3SVC",
        "sshd"
    ]
    for service in services_to_disable:
        print(f"Stopping {service}")
        subprocess.run(f'sc stop {service}', shell=True, check=True)
        subprocess.run(f'sc config {service} start= disabled', shell=True, check=True)
    print("Disabled and stopped unnecessary services.")

if __name__ == "__main__":
    manage_services()
