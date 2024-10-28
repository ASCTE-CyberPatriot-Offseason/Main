import subprocess

def configure_audit_policies():
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
    command_template = 'auditpol /set /subcategory:"{}" /success:enable /failure:enable'
    for policy in audit_policies:
        command = command_template.format(policy)
        subprocess.run(command, shell=True, check=True)
        print(f"{command} executed")

if __name__ == "__main__":
    configure_audit_policies()
