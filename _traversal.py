import glob
import os 
import sys

dir_path = glob.glob(sys.argv[1]+"/*")
for file_name in dir_path:
    if("apk" in file_name or "APK" in file_name):
        #print (file_name)
        #command = "python3 ./find_call_func.py {}".format(file_name)
        command = "python3 ./check_callable_service.py {} 2>/dev/null" .format(file_name)
        os.system(command)


