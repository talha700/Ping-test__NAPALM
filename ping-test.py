from napalm import get_network_driver
import subprocess
import time


#Give here the filename with one IP on each line for ping test 
FILE_FOR_TEST = ""


driver = get_network_driver("ios")

device = driver(hostname="192.168.122.120",
                username="admin",
                password="admin")

device.open()

device.load_merge_candidate(filename="conf.txt")
print("Commiting Changes...\n")
device.commit_config()
print("Committed.")

time.sleep(6)

print("Testing....\n")
with open(FILE_FOR_TEST) as f:
    data = f.read().splitlines()


for device_ip in data:
    response = subprocess.Popen(['timeout','5','ping' ,'-c','2', device_ip],stdout=subprocess.PIPE)
    response.wait()
    if response.returncode != 0:
        print(f"{device_ip} NOT REACHABLE !!")
        print("*"*40)
        print("TEST FAILED.....................ROLLING BACK !")
        device.rollback()
        exit()
    else:
        print(f"{device_ip} Reachable.")

print("="*40)
print("TEST Passed...Changes are kept.")

device.close()

