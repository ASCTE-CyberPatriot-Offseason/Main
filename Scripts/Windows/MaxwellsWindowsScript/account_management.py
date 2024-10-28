import subprocess

def disable_accounts():
    commands = [
        'net user admin /active:no',
        'net user guest /active:no'
    ]
    for command in commands:
        subprocess.run(command, shell=True, check=True)
        print(f"{command} executed")

if __name__ == "__main__":
    disable_accounts()
