from androguard.misc import AnalyzeAPK
from bs4 import BeautifulSoup
import sys

if ( len(sys.argv)>1):
    APK_FILE = sys.argv[1]
else:
    APK_FILE="../SYSTEM_APPS/AiAgent.apk"

#APK_FILE="../SYSTEM_APPS/AiAgent.apk"
#APK_FILE="../SYSTEM_FRAMEWORK/framework/vivo-services.jar"

print(">>> Analyzer APK : [%s]"%(APK_FILE))

a, d, dx = AnalyzeAPK(APK_FILE)
all_methods = dx.get_methods()
all_classes = dx.get_classes()
service_lists = a.get_services()
manifestData = str(a.get_android_manifest_axml().get_xml())
soup = BeautifulSoup(manifestData, 'html.parser')
manifest = soup.find_all("manifest")
m = str(manifestData)
UserId = m[m.find("android:sharedUserId"):m.find("android:sharedUserId")+40]
if ("system" in UserId ):
    sys.exit(0)
else:
    print("[+] >>> [%s] app " %(UserId))


packageName = m[m.find("package=")+8: m.find("package=")+50]
packageName = packageName.split(" ")[0].strip("\"")
print("[+] >>> packageName [ %s ] " %(packageName))

targetClasses = [] 

activities = soup.find_all("activity")
services   = soup.find_all("service")
receivers  = soup.find_all("receiver")

targetClasses = activities + services + receivers 
targetStructure =[]

for target in targetClasses:
    tmpDict = {} 
    tmpDict['class_name'] = ""
    tmpDict['actions'] = []
    tmpDict['permission'] = ""
    tmpDict['detection'] = []
    
    if (target.has_attr("android:name")):
        tmpDict['class_name'] = target["android:name"] 
        for action in target.find_all("action"):
            if(action.has_attr("android:name")):
                action_name = action["android:name"]
                tmpDict['actions'].append(action_name)
            
    if(target.has_attr("android:permission")):
        permission = target["android:permission"]
        tmpDict['permission'] = permission
    targetStructure.append(tmpDict)
#print(targetStructure)

def checkPermAuth(permission):
    stdout_string =""
    if( permission !="" ):
        command_string = 'adb shell "pm list permissions -f |grep %s -A 10 |grep protection | head -n 1"'% (permission)
        output = subprocess.check_output(command_string, shell=True)
        output = output.decode("utf-8").strip()
        if(len(str(output)) < 2 ):
            stdout_string+="[can not find permission]"
        else:
            stdout_string+="[%s]" %(output)
    else :
        stdout_string+="[no permission]"
    return (stdout_string)


FilterStr = ['chmod ','.tar','.zip','unzip ','mv ','cp ','sh -c','/sdcard/', 'rm -', 'tar ' ]
MethodsStr = ['File;->create','File;-><init>' ,'loadLibrary','Runtime;->exec']
#File-> 
functionTraveler = []
detections = {}
def getAnalyzer(class_name, method , depth=0 ):
    #print("----> ",end="")
    #print(method)
    #print(depth)
    if(method.is_external() or depth > 10 ): return 0
    
    tuples = method.get_xref_to()
    for _, m, off in method.get_xref_to() :
        
        ## recursive call
        if m not in functionTraveler :
            functionTraveler.append(m)
            getAnalyzer(class_name, m, depth=depth+1)
    
    method_ctx = method.get_method()
    if not method_ctx.get_code(): return 0
    tmpList = [] 
    for instruction in method_ctx.get_instructions():
        if("const-string" in instruction.get_name() ):
            for operand in instruction.get_operands():
                #print(operand)
                for t in FilterStr :
                    if (str(t) in str(operand)):
                        #print(t)
                        tmpList.append("string: "+str(operand))
                        #retDetection.append(str(operand))
        if("invoke-virtual" in instruction.get_name()):
            for operand in instruction.get_operands():
                for t in MethodsStr:
                    if (str(t) in str(operand)):
                        tmpList.append("invoke-call: " + str(operand))
        
        if("invoke-direct" in instruction.get_name()):
            for operand in instruction.get_operands():
                for t in MethodsStr:
                    if (str(t) in str(operand)):
                        tmpList.append("invoke-call: " + str(operand))

    #print(tmpList)
    if(tmpList):
        detections[class_name].extend(tmpList)

target_name ="com.vivo.agent.view.activities.qickcommand.SelectOfficialSkillsActivity"

def serachString(target_name):
    for cls in dx.find_classes(".%s" %(target_name),no_external=True):
        #print(cls.get_methods())
        for method_ctx in cls.get_methods():

            if ( "onCreate" in str(method_ctx.get_method()) or "onStart" in str(method_ctx.get_method()) or "onReceive"  in str(method_ctx.get_method()) ):
                functionTraveler=[]
                detections[target_name] = []
                getAnalyzer(target_name , method_ctx)
                if(detections[target_name]):
                    return 1
    return 0



print("---------------------------------------------------------------------------")
for target in targetStructure:
    #target['class_name']
    #print(target['class_name'])
    if ( serachString(target['class_name']) ):
        
        print("[+] class: [%s], perm: [%s] " %(target['class_name'], target['permission'] ))
        for result in detections[target['class_name']]:
            print(result)
print("---------------------------------------------------------------------------")
    
