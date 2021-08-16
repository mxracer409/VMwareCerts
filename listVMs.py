import os
import requests
import urllib3
import json
import getpass
import time
#from vmware.vapi.vsphere.client import create_vsphere_client
#to add a progress bar if desired
#from tqdm import tqdm (make sure tqdm is installed 
# session.verify = self.args.cert_path- pip install tqdm)
#for i in tqdm(range(1000)): 
# do for loop

#Try to import the VMware Python SDK, if fail, pip install the python SDK, wait 60 seconds, try again. 
t = False
count = 0
while t == False:
    try:
        from vmware.vapi.vsphere.client import create_vsphere_client
        t = True
        print('vmware sdk present')
        break
    except ImportError as e:
        if count == 0:
            print('no vmware sdk present. installing with pip')
            os.system('pip install --upgrade pip setuptools') # this will excute a cli cmd
            os.system('pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git')
            time.sleep(60)
            count += 1
        else:
            print('still installing vmware python sdk')



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

def createCSRConfigFiles(hostNames):
    path = os.getcwd()
    try:
        fileIn = open("openssl_template.cfg", "rt")
        print("opening the open SSL cfg template file")
    except Exception as e:
        print("Can't open openssl_template.cfg file to read, exiting")
        exit()
    
    for name in hostNames:
        try:
            outPath = os.path.join(os.getcwd(),'HostCSR', name)
            #os.mkdir(outPath)
            os.makedirs(outPath, exist_ok=True)
            os.chdir(outPath)
            fileOut = open(name, "wt")
            for line in fileIn:
                if "commonName" in line:
                    fileOut.write(line.replace('<variable>', name))
                else:
                    fileOut.write(line)
            fileOut.close()

        except Exception as e: 
            print("directory might already exist, exiting")
            print(e)
            exit()
        
        os.chdir(path)

    fileIn.close()
    return print('generated an openssl cfg file for each host located here: ' + os.getcwd() + '\HostCSR')

def generateCSRandKeyFiles(hostNames):
    #hostNames not used right now... can remove from input)
    parentPath = os.getcwd()
    path = os.path.join(parentPath, 'HostCSR')
    os.chdir(path)
    for folder in os.listdir(os.getcwd()):
        newPath = os.path.join(path, folder)
        os.chdir(newPath)
        openSSLfile = folder
        #using full path to OpenSSL install location right now C:\"Program Files"\OpenSSL-Win64\bin\openssl
        try: 
            openSSLlocation = 'C:\\"Program Files"\\OpenSSL-Win64\\bin\\openssl.exe'
            openSSLcmdEXEcommand = '{} req -new -nodes -out {}.csr -keyout {}-orig.key -config {}'.format(openSSLlocation, openSSLfile, openSSLfile, openSSLfile)
            os.system(openSSLcmdEXEcommand)
            print(".CSR and .Key file successfully created at {}".format(newPath))
        except Exception as e:
            print("error in openSSL CSR and Key file creation - more details")
            print(e)
            exit()


if __name__ == "__main__":
    
    vCenterHostIP = '192.168.2.4'
    usernameValue = 'administrator@vsphere.local'
    password = 'Go2atc4labs!'
    #password = getpass.getpass()
    
    vsphere_client = connectToVcenterWithSDK(vCenterHostIP, usernameValue, password)
    
    hostNames = getESXiHostNames(vsphere_client)
    vmNames = getVMNames(vsphere_client)
    vsphere_client.session.close

    createCSRConfigFiles(hostNames)
    #createCSRConfigFiles(['esx1', 'esxi2', 'esxi3'])

    generateCSRandKeyFiles(hostNames)