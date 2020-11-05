import sys

#from androguard.core.bytecodes.apk import APK
#from androguard.core.bytecodes.dvm import DalvikVMFormat
#from androguard.core.bytecodes.dvm import ClassDefItem

from androguard.misc import AnalyzeAPK

def print_k(msg, info='+'):
        print("[{}] {}".format(info,msg))

def usage():
    print_k("python ./{} [apk_file]".format(sys.argv[0]))

def find_function_call(method_, key_func="/"):
    if method_.is_external():
        return 0
    method = method_.get_method()
    if not method.get_code(): return 0
    
    instruction_tmp = []
    for instruction in method.get_instructions():
        if("const-string" in instruction.get_name()):
            #print (method)
            #print (instruction)
            instruction_tmp.append(instruction.get_operands())
        
        for operand in instruction.get_operands():
            for op in operand:
                if key_func in str(op):
                    if(instruction_tmp):
                        print_k(op,"!")
                        print_k(method,"->")
                        print_l(instruction_tmp)
    return 0

def init(apk_file):
    print_k(apk_file)
    try:
        pass
        #dalvik_ctx = DalvikVMFormat( APK(apk_file) )
    except :
        print_k("DalvicVMFormat Error","-")
        sys.exit();
    a,d,dx = AnalyzeAPK(apk_file)
    methods = dx.get_methods()
    #methods = dalvik_ctx.get_methods()
    #class = "com.oppo.gallery3d.o.a"
    return methods 

def print_l(list_data):
    for msg in list_data :
        print ("\t{}".format(msg))

def scan_methods(methods, key_func="/"):
    for method in methods:
        find_function_call(method, key_func)
                     
def main(): 
    if(len(sys.argv) > 1):
        apk_name = sys.argv[1]
    else:
        usage()
        sys.exit(1)

    methods = init(apk_name)
    scan_methods(methods, "Runtime;->exec")

if __name__ == "__main__":
    main()

