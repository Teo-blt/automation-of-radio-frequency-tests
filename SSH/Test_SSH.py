#!/usr/bin/env python
import paramiko
import time

ip_address = "192.168.4.228"
username = "root"
password = "root"

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username, password=password)
print("Successfully connected to", ip_address)

remote_connection = ssh_client.invoke_shell()

remote_connection.send("configure terminal" + "\n")

for vlan in range(2, 11):
    print("Creating VLAN number " + str(vlan))
    remote_connection.send("vlan " + str(vlan) + "\n")
    remote_connection.send("name VLAN " + str(vlan) + "\n")
    time.sleep(0.5)

remote_connection.send("end\n")

time.sleep(1)
output = remote_connection.recv(65535)
print(output)

ssh_client.close
