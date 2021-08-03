import os
import requests
import urllib3
import json
import getpass
from vmware.vapi.vsphere.client import create_vsphere_client
#to add a progress bar if desired
#from tqdm import tqdm (make sure tqdm is installed 
# session.verify = self.args.cert_path- pip install tqdm)
#for i in tqdm(range(1000)): 
# do for loop


def connectToVcenterWithSDK(vCenterHostIP, usernameValue, password): 
    session = requests.session()
    session.verify = False
    session.trust_env = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    vsphere_client = create_vsphere_client(server=vCenterHostIP, username = usernameValue, password = password, session=session)    
    return vsphere_client

def getESXiHostNames(vsphere_client):

    listHosts = vsphere_client.vcenter.Host.list()

    strippedlistESX = []
    listtoStr = ' '.join(map(str, listHosts))
    splitlistHosts = listtoStr.split(", ")
    for i in splitlistHosts:
        if i != None and "name" in i:
            i = i.lstrip("name : ")
            strippedlistESX.append(i)
            #print(i)
    return strippedlistESX

def getVMNames(vsphere_client):

    listVMs = vsphere_client.vcenter.VM.list()
        
    strippedlistVMs = []
    listtoStr = ' '.join(map(str, listVMs))
    splitlistVMs = listtoStr.split(", ")
    for i in splitlistVMs: 
        if i != None and "name" in i:
            i = i.lstrip("name : ")
            strippedlistVMs.append(i)
            #print(i)
    return strippedlistVMs

if __name__ == "__main__":
    
    vCenterHostIP = '192.168.2.4'
    usernameValue = 'administrator@vsphere.local'
    password = 'Go2atc4labs!'
    #password = getpass.getpass()
    
    vsphere_client = connectToVcenterWithSDK(vCenterHostIP, usernameValue, password)
    
    hostNames = getESXiHostNames(vsphere_client)
    vmNames = getVMNames(vsphere_client)

    vsphere_client.session.close