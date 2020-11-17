import sys
import binascii
import sys
from bs4 import BeautifulSoup
from androguard.misc import AnalyzeAPK

#apk_file="com.coloros.gallery3d.apk"
if ( len(sys.argv) < 2 ):
    apk_file="BackupAndRestore.apk"
else:
    apk_file=sys.argv[1]
#apk_file="BackupAndRestore.apk"
a, d, dalvik_ctx = AnalyzeAPK(apk_file)
#print("[+] %s init Done" %(apk_file))

signed_flag = True
for cert in a.get_certificates():
#     cert.sha1  # the sha1 fingerprint
#     cert.sha256  # the sha256 fingerprint
#     cert.issuer.human_friendly  # issuer
#     cert.subject.human_friendly  # subject, usually the same
#     cert.hash_algo  # hash algorithm
#     cert.signature_algo  # Signature algorithm
#     cert.serial_number  # Serial number
#     cert.contents  # The DER coded bytes of the certificate itself
    #oppo_finger ="57 AA BE 69 96 0A 90 8A 74 68 28 45 67 94 FB FB 66 64 0B A2"
    oppo_finger  ="28 3D 60 DD CD 20 C5 6E A1 71 9C E9 05 27 F1 23 5A E8 0E FA"
    #print(oppo_finger)
    print(str(cert.sha1_fingerprint))
    if(str(oppo_finger) == str(cert.sha1_fingerprint) ):
        signed_flag=True
        print("----------------------------------------------------")
        print("[+] %s init Done" %(apk_file))
        print("[+] is priv-app [True] ")
        break
    else:
        signed_flag=False

        #print("[-] is priv-app [False]")
        break
if(signed_flag ==False):
    sys.exit(1)

if( not a.is_signed_v2() or not a.is_signed_v3() ):
    print("[!] APK [%s] is not signed from v2, v3" %(apk_file))

service_lists = a.get_services()
manifestData = str(a.get_android_manifest_axml().get_xml())
soup = BeautifulSoup(manifestData, 'html.parser')
for service_name in service_lists:
    tmpData       =""
    intent_filter =[]
    permission    = ""
    exported      = False
    has_ifilter   = False 
    
    service_name = service_name.split(".")[-1]
    services    = soup.find_all("service")
    for service in services :
        if (service.has_attr('android:name')):
            if (service_name in service['android:name']): pass
            else: continue
                
        if (service.has_attr('android:permission')):
            permission =  service['android:permission']
        else: permission=""
        
        if (service.has_attr('android:exported')):
            if ( service['android:exported'] == "true"): exported=True
        else: exported = False
        
        # intent filter 
        if (len(service.find_all('intent-filter')) > 0 ):
            has_ifilter = True 
            intents = service.find_all('intent-filter')
            for intent in intents :
                actions = intent.find_all('action')
                #print(actions)
                for action in actions:
                    #print(action)
                    intent_filter.append(action['android:name'])
                    
    if(exported==True or has_ifilter == True ):
        print("[!] (exported=[%s]) ->" %(exported), end=' ')
        print(service_name, end='')
        print(" (perm:[%s])"% permission, end="->")
        import subprocess
        if( permission !="" ):
            command_string = 'adb shell "pm list permissions -f |grep %s -A 10 |grep protection | head -n 1"'% (permission)
            output = subprocess.check_output(command_string, shell=True)
            output = output.decode("utf-8").strip()
            if(len(str(output)) < 2 ):
                print("[can not find permission]")
            else:
                print("[%s]" %(output))
        else : print("[no permission]")
        for intent in intent_filter:
            print("\t[->]intent-filter action: [%s] "% intent)
                    
receivers = a.get_receivers()
for receive_name in receivers:
    print("[+] Receiver : " + receive_name )
