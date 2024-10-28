import subprocess

def uninstall_malicious_software():
    software_list = ["Wireshark", "Netcap", "CCleaner"]
    powershell_script = """
    $softwareList = @{software_list}
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
    """.format(software_list=", ".join([f'"{software}"' for software in software_list]))
    subprocess.run(["powershell", "-Command", powershell_script], check=True)
    print("Malicious software uninstallation attempted.")

if __name__ == "__main__":
    uninstall_malicious_software()
