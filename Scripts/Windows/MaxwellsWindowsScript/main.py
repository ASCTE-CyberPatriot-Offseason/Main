
print("Begin computer fixing ;)")

print("updating defender")
input("press inter to begin... ")
import defender_updates
defender_updates.check_install_updates()

print("configuring firewall settings")
input("press inter to begin... ")
import firewall_config
firewall_config.enable_firewall()

print("fix audit policies")
input("press inter to begin... ")
import audit_policies
audit_policies.configure_audit_policies()

print("changing password policies")
input("press inter to begin... ")
import password_policies

print("running service management")
input("press inter to begin... ")
import service_manaement

print("running software management")
input("press inter to begin... ")
import software_management

print("changing uac settings")
input("press inter to begin... ")
import uac_settings

print("WARNING! RUNNING FILE CLEANER. HOPE AND PRAY")
input("press inter to begin... ")
import file_cleaner


print("done. didn't run account mgmt, btw")