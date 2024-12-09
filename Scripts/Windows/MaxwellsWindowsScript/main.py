
print("Begin computer fixing ;)")

print("running defender scan")
input("press enter to begin... ")
import defender_updates
defender_updates.run_windows_defender_scan()

print("configuring firewall settings")
input("press enter to begin... ")
import firewall_config
firewall_config.enable_firewall()

print("fix audit policies")
input("press enter to begin... ")
import audit_policies
audit_policies.configure_audit_policies()

print("changing password policies")
input("press enter to begin... ")
import password_policies
password_policies.configure_password_policies()

print("running service management")
input("press enter to begin... ")
import service_manaement
service_manaement.manage_services()

print("running software management")
input("press enter to begin... ")
import software_management
software_management.deleteDirectories()

print("changing uac settings")
input("press enter to begin... ")
import uac_settings
uac_settings.configure_uac()

print("WARNING! RUNNING FILE CLEANER. HOPE AND PRAY")
input("press enter to begin... ")
import file_cleaner


print("done. didn't run account mgmt, btw")
print("if you want ot try and update (might not work), type (y)yes")
ans = input("try update, (y)yes or no? ")
if ans == "y":
    print("attempting update")
    defender_updates.check_install_updates()
else:
    print("skipped. the end. if it wasn't enough, blame maxwell")