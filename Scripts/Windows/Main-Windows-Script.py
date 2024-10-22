"""
This is the main script for Windows.
All task for this script will be pulled from the windows cyberPatriot checklist.
order of the task is not yet determined.(possibly no order)
"""


import subprocess
import os
import fnmatch

#enable firewall
subprocess.run(["powershell", "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True"])
print("Firewall enabled.")

print("audit policies")
# List of audit policies to configure
audit_policies = [
    "Audit account logon events",
    "Audit account management",
    "Audit directory service access",
    "Audit logon events",
    "Audit object access",
    "Audit policy change",
    "Audit privilege use",
    "Audit process tracking",
    "Audit system events"
]

# Command template to set audit policy
command_template = 'auditpol /set /subcategory:"{}" /success:enable /failure:enable'

# Loop through each policy and set it to log both successes and failures
for policy in audit_policies:
    command = command_template.format(policy)
    subprocess.run(command, shell=True, check=True)
    print(command)

print("Audit policies updated to log both successes and failures.")

print("password policies")
#change password policies
password_policies = [
    "net accounts /minpwlen:8",  # Minimum password length
    "net accounts /maxpwage:30",  # Maximum password age (days)
    "net accounts /minpwage:1",  # Minimum password age (days)
    "net accounts /uniquepw:5",  # Number of unique passwords before reuse
    "net accounts /lockoutthreshold:5",  # Account lockout threshold
    "net accounts /lockoutduration:30",  # Account lockout duration (minutes)
    "net accounts /lockoutwindow:30"  # Reset account lockout counter after (minutes)
]

for policy in password_policies:
    subprocess.run(policy, shell=True, check=True)
    print(policy)
print("Password policies updated.")
#change UAC (user account control) settings
print("UAC settings")
subprocess.run('powershell.exe -Command "Set-ItemProperty -Path HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System -Name ConsentPromptBehaviorAdmin -Value 2"', shell = True, check = True)
print("UAC settings updated.")

#disable admin and guest account
print("Disabling guest and admin account")
commands = [
    'net user admin /active:no',
    'net user guest /active:no'
]

for command in commands:
    subprocess.run(command, shell=True, check=True)

print("Admin and Guest accounts have been disabled.")


#remove malicous software
# List of software to uninstall
software_list = ["Wireshark", "Netcap", "CCleaner"]

# PowerShell script to uninstall software
powershell_script = """
$softwareList = @{}
$installedSoftware = Get-WmiObject -Class Win32_Product

foreach ($software in $softwareList) {{
    $app = $installedSoftware | Where-Object {{ $_.Name -like "*$software*" }}
    if ($app) {{
        try {{
            $app.Uninstall()
            Write-Output "Uninstalled: $($app.Name)"
        }} catch {{
            Write-Output "Error uninstalling $($app.Name): $_"
        }}
    }} else {{
        Write-Output "$software is not installed."
    }}
}}
""".format(", ".join([f'"{software}"' for software in software_list]))

# Run the PowerShell script
subprocess.run(["powershell", "-Command", powershell_script], check=True)

# PowerShell command to update Google Chrome
powershell_command = """
$chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
if (Test-Path $chromePath) {
    $updateCommand = "$chromePath --check-for-update-interval=1"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $updateCommand -Verb RunAs
    Write-Output "Google Chrome update initiated."
} else {
    Write-Output "Google Chrome is not installed."
}
"""

# Run the PowerShell command
subprocess.run(["powershell", "-Command", powershell_command], check=True)

# PowerShell command to update Firefox
powershell_command_firefox = """
$firefoxPath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
if (Test-Path $firefoxPath) {
    $updateCommand = "$firefoxPath -silent -update"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c", $updateCommand -Verb RunAs
    Write-Output "Mozilla Firefox update initiated."
} else {
    Write-Output "Mozilla Firefox is not installed."
}
"""

# Run the PowerShell command for Firefox
subprocess.run(["powershell", "-Command", powershell_command_firefox], check=True)

# List of services to stop and disable
services = [
    "TermService",  # RDP
    "SharedAccess",  # ICS
    "UmRdpService",  # RDP UserMode
    "ftpsvc",  # Windows FTP service
    "RemoteRegistry",  # Remote Registry
    "SessionEnv",  # RD Configuration
    "SSDPSRV",  # SSDP Discovery
    "upnphost",  # UPnP Device Host
    "TermService",  # Remote Desktop
    "W3SVC",  # WWW Publishing Service
    "TermService",  # remote desktop
    "sshd"  # ssh
]

for service in services:
    print(f"Stopping {service} service")
    subprocess.run(f'sc stop {service}', shell=True, check=True)
    print(f"Disabling {service} service")
    subprocess.run(f'sc config {service} start= disabled', shell=True, check=True)

# Disable remote desktop
print("Disabling Remote Desktop")
subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f', shell=True, check=True)
print("Remote Desktop has been disabled.")

# List of PowerShell commands to block the specified ports
commands = [
    'New-NetFirewallRule -DisplayName "Block RDP" -Direction Inbound -LocalPort 3389 -Protocol TCP -Action Block',
    'New-NetFirewallRule -DisplayName "Block SSH" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Block',
    'New-NetFirewallRule -DisplayName "Block TelNet" -Direction Inbound -LocalPort 23 -Protocol TCP -Action Block',
    'New-NetFirewallRule -DisplayName "Block SNMP 161" -Direction Inbound -LocalPort 161 -Protocol UDP -Action Block',
    'New-NetFirewallRule -DisplayName "Block SNMP 162" -Direction Inbound -LocalPort 162 -Protocol UDP -Action Block',
    'New-NetFirewallRule -DisplayName "Block LDAP" -Direction Inbound -LocalPort 389 -Protocol TCP -Action Block',
    'New-NetFirewallRule -DisplayName "Block FTP Command" -Direction Inbound -LocalPort 21 -Protocol TCP -Action Block',
    'New-NetFirewallRule -DisplayName "Block FTP Data" -Direction Inbound -LocalPort 20 -Protocol TCP -Action Block'
]

# Execute each command using subprocess.run
for command in commands:
    subprocess.run(["powershell", "-Command", command], check=True)
    

try:
    # Command to run a quick scan using Windows Defender
    command = ["powershell", "Start-MpScan", "-ScanType", "QuickScan"]
        
    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
        
    # Check if the command was successful
    if result.returncode == 0:
        print("Quick scan completed successfully.")
        print(result.stdout)
    else:
        print("Quick scan failed.")
        print(result.stderr)
except Exception as e:
    print(f"An error occurred: {e}")