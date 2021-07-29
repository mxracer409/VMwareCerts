import os
import requests
import urllib3
import json
import getpass

from vmware.vapi.vsphere.client import create_vsphere_client

vCenterHostIP = '192.168.2.4'
usernameValue = 'administrator@vsphere.local'
#password = getpass.getpass()
password = 'Go2atc4labs!'

session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
vsphere_client = create_vsphere_client(server=vCenterHostIP, username = usernameValue, password = password, session=session)

listVMs = vsphere_client.vcenter.VM.list()
listHosts = vsphere_client.vcenter.Host.list()

def getESXiHostNames():
    strippedlistESX = []
    listtoStr = ' '.join(map(str, listHosts))
    splitlistHosts = listtoStr.split(", ")
    for i in splitlistHosts:
        if i != None and "name" in i:
            print(i)
            strippedlistESX.append(i)
    return strippedlistESX

def getVMNames():
#For loop for multiple hosts 
    strippedlistVMs = []
    listtoStr = ' '.join(map(str, listVMs))
    splitlistVMs = listtoStr.split(", ")
    for i in splitlistVMs: 
        if i != None and "name" in i:
            print(i)
            strippedlistVMs.append(i)
    return strippedlistVMs

if __name__ == "__main__":
    getESXiHostNames()
    #getVMNames()