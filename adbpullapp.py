#/usr/bin/python2.8
import subprocess 

def getpmList():
    print("pm list packages -f -U |grep 1000")
    

def download(a1, a2):
    cmd = "adb pull %s ./systemAPPS/%s" % (a1, a2)
    print (cmd)
    subprocess.check_output(cmd, shell=True)


getpmList()

f = open("systempackages.txt","r") 
for line in f.readlines():
    package_name = ""
    paackage_path = ""
    if (line.find("package:") >=0 and line.find("uid:1000\x0a")>=0):
        package_path = line.split("package:")[1].split("=")[0]
        package_name = line.split("=")[1].split("uid:1000")[0]
        
        download(package_path, package_name)

