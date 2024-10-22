"""
This is the main script for Windows.
All task for this script will be pulled from the windows cyberPatriot checklist.
order of the task is not yet determined.(possibly no order)
"""


import subprocess

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
    

# List of commands to stop and disable services might be overlap was coppied and pasted from previous code
stop_disable_commands = [
    'sc stop tlntsvr',
    'sc config tlntsvr start= disabled',
    'sc stop msftpsvc',
    'sc config msftpsvc start= disabled',
    'sc stop snmptrap',
    'sc config snmptrap start= disabled',
    'sc stop ssdpsrv',
    'sc config ssdpsrv start= disabled',
    'sc stop termservice',
    'sc config termservice start= disabled',
    'sc stop sessionenv',
    'sc config sessionenv start= disabled',
    'sc stop remoteregistry',
    'sc config remoteregistry start= disabled',
    'sc stop Messenger',
    'sc config Messenger start= disabled',
    'sc stop upnphos',
    'sc config upnphos start= disabled',
    'sc stop WAS',
    'sc config WAS start= disabled',
    'sc stop RemoteAccess',
    'sc config RemoteAccess start= disabled',
    'sc stop mnmsrvc',
    'sc config mnmsrvc start= disabled',
    'sc stop NetTcpPortSharing',
    'sc config NetTcpPortSharing start= disabled',
    'sc stop RasMan',
    'sc config RasMan start= disabled',
    'sc stop TabletInputService',
    'sc config TabletInputService start= disabled',
    'sc stop RpcSs',
    'sc config RpcSs start= disabled',
    'sc stop SENS',
    'sc config SENS start= disabled',
    'sc stop EventSystem',
    'sc config EventSystem start= disabled',
    'sc stop XblAuthManager',
    'sc config XblAuthManager start= disabled',
    'sc stop XblGameSave',
    'sc config XblGameSave start= disabled',
    'sc stop XboxGipSvc',
    'sc config XboxGipSvc start= disabled',
    'sc stop xboxgip',
    'sc config xboxgip start= disabled',
    'sc stop xbgm',
    'sc config xbgm start= disabled',
    'sc stop SysMain',
    'sc config SysMain start= disabled',
    'sc stop seclogon',
    'sc config seclogon start= disabled',
    'sc stop TapiSrv',
    'sc config TapiSrv start= disabled',
    'sc stop p2pimsvc',
    'sc config p2pimsvc start= disabled',
    'sc stop simptcp',
    'sc config simptcp start= disabled',
    'sc stop fax',
    'sc config fax start= disabled',
    'sc stop Msftpsvc',
    'sc config Msftpsvc start= disabled',
    'sc stop iprip',
    'sc config iprip start= disabled',
    'sc stop ftpsvc',
    'sc config ftpsvc start= disabled',
    'sc stop RasAuto',
    'sc config RasAuto start= disabled',
    'sc stop W3svc',
    'sc config W3svc start= disabled',
    'sc stop Smtpsvc',
    'sc config Smtpsvc start= disabled',
    'sc stop Dfs',
    'sc config Dfs start= disabled',
    'sc stop TrkWks',
    'sc config TrkWks start= disabled',
    'sc stop MSDTC',
    'sc config MSDTC start= disabled',
    'sc stop ERSvc',
    'sc config ERSvc start= disabled',
    'sc stop NtFrs',
    'sc config NtFrs start= disabled',
    'sc stop Iisadmin',
    'sc config Iisadmin start= disabled',
    'sc stop IsmServ',
    'sc config IsmServ start= disabled',
    'sc stop WmdmPmSN',
    'sc config WmdmPmSN start= disabled',
    'sc stop helpsvc',
    'sc config helpsvc start= disabled',
    'sc stop Spooler',
    'sc config Spooler start= disabled',
    'sc stop RDSessMgr',
    'sc config RDSessMgr start= disabled',
    'sc stop RSoPProv',
    'sc config RSoPProv start= disabled',
    'sc stop SCardSvr',
    'sc config SCardSvr start= disabled',
    'sc stop lanmanserver',
    'sc config lanmanserver start= disabled',
    'sc stop Sacsvr',
    'sc config Sacsvr start= disabled',
    'sc stop TermService',
    'sc config TermService start= disabled',
    'sc stop uploadmgr',
    'sc config uploadmgr start= disabled',
    'sc stop VDS',
    'sc config VDS start= disabled',
    'sc stop VSS',
    'sc config VSS start= disabled',
    'sc stop WINS',
    'sc config WINS start= disabled',
    'sc stop CscService',
    'sc config CscService start= disabled',
    'sc stop hidserv',
    'sc config hidserv start= disabled',
    'sc stop IPBusEnum',
    'sc config IPBusEnum start= disabled',
    'sc stop PolicyAgent',
    'sc config PolicyAgent start= disabled',
    'sc stop SharedAccess',
    'sc config SharedAccess start= disabled',
    'sc stop SSDPSRV',
    'sc config SSDPSRV start= disabled',
    'sc stop Themes',
    'sc config Themes start= disabled',
    'sc stop upnphost',
    'sc config upnphost start= disabled',
    'sc stop nfssvc',
    'sc config nfssvc start= disabled',
    'sc stop nfsclnt',
    'sc config nfsclnt start= disabled',
    'sc stop MSSQLServerADHelper',
    'sc config MSSQLServerADHelper start= disabled',
    'sc stop SharedAccess',
    'sc config SharedAccess start= disabled',
    'sc stop UmRdpService',
    'sc config UmRdpService start= disabled',
    'sc stop SessionEnv',
    'sc config SessionEnv start= disabled',
    'sc stop Server',
    'sc config Server start= disabled',
    'sc stop TeamViewer',
    'sc config TeamViewer start= disabled',
    'sc stop TeamViewer7',
    'sc config start= disabled',
    'sc stop HomeGroupListener',
    'sc config HomeGroupListener start= disabled',
    'sc stop HomeGroupProvider',
    'sc config HomeGroupProvider start= disabled',
    'sc stop AxInstSV',
    'sc config AXInstSV start= disabled',
    'sc stop Netlogon',
    'sc config Netlogon start= disabled',
    'sc stop lltdsvc',
    'sc config lltdsvc start= disabled',
    'sc stop iphlpsvc',
    'sc config iphlpsvc start= disabled',
    'sc stop AdobeARMservice',
    'sc config AdobeARMservice start= disabled'
]

# Execute stop and disable commands
for command in stop_disable_commands:
    subprocess.run(['cmd.exe', '/c', command], check=True)

# List of commands to start and enable services
start_enable_commands = [
    'sc start wuauserv',
    'sc config wuauserv start= auto',
    'sc start EventLog',
    'sc config EventLog start= auto',
    'sc start MpsSvc',
    'sc config MpsSvc start= auto',
    'sc start WinDefend',
    'sc config WinDefend start= auto',
    'sc start WdNisSvc',
    'sc config WdNisSvc start= auto',
    'sc start Sense',
    'sc config Sense start= auto',
    'sc start Schedule',
    'sc config Schedule start= auto',
    'sc start SCardSvr',
    'sc config SCardSvr start= auto',
    'sc start ScDeviceEnum',
    'sc config ScDeviceEnum start= auto',
    'sc start SCPolicySvc',
    'sc config SCPolicySvc start= auto',
    'sc start wscsvc',
    'sc config wscsvc start= auto'
]



# Execute start and enable commands
for command in start_enable_commands:
    subprocess.run(['cmd.exe', '/c', command], check=True)
    
    
    
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

#check for windows update
try:
    print("Checking for updates...")
    subprocess.run(["usoclient", "StartScan"], check=True)
    print("Update check initiated.")
except subprocess.CalledProcessError as e:
    print(f"Failed to check for updates: {e}")

try:
    print("Installing updates...")
    subprocess.run(["usoclient", "StartInstall"], check=True)
    print("Update installation initiated.")
except subprocess.CalledProcessError as e:
    print(f"Failed to install updates: {e}")

"""
things to add:
    account managment
    file manangment is a maybe based on if I want to risk deleting cyber patriot files
    malware removal
"""