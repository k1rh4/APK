import glob
import os 
import sys

dir_path = glob.glob(sys.argv[1]+"/*")
for file_name in dir_path:
    if("apk" in file_name or "APK" in file_name):
        #print (file_name)
        command = "python ./main.py {}".format(file_name)
        os.system(command)


