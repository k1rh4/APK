import sys

#from androguard.core.bytecodes.apk import APK
#from androguard.core.bytecodes.dvm import DalvikVMFormat
#from androguard.core.bytecodes.dvm import ClassDefItem

from androguard.misc import AnalyzeAPK
def init(apk_file):
    print_k(apk_file)
    a,d,dx = AnalyzeAPK(apk_file)
    methods = dx.get_methods()
    return methods 

def usage()                 : print_k("python ./{} [apk_file]".format(sys.argv[0]))
def print_k(msg, info='+')  : print("[{}] {}".format(info,msg))
def print_l(list_data)      : 
    for msg in list_data : 
        print ("\t{}".format(msg))

def find_function_call(method_, key_func=['']):
    if method_.is_external():
        return 0
    method = method_.get_method()
    if not method.get_code(): return 0
    
    instruction_tmp = []
    for instruction in method.get_instructions():
        if("const-string" in instruction.get_name()):
            
            if "/cache/" in str(instruction.get_operands()):
                print_k(method)

            if "/cache/" in str(instruction.get_operands()) and \
                    ".sh" in str(instruction.get_operands()) :
                print_k(method)
                print_k(str(instruction.get_operands()))
            
            if "/sdcard/" in str(instruction.get_operands()) and \
                    ".sh" in str(instruction.get_operands()) :
                print_k(method)
                print_k(str(instruction.get_operands()))
            
            if "/data/local/" in str(instruction.get_operands()) and \
                    ".sh" in str(instruction.get_operands()) :
                print_k(method)
                print_k(str(instruction.get_operands()))

        '''
        for operand in instruction.get_operands():
            for op in operand:
                if key_func in str(op):
                    print_k(op,"!")
                    return instruction_tmp
        '''
    return 0


def scan_methods(methods):
    for method in methods:
        inst_list = find_function_call(method)
        if inst_list :
            print_k(method,"->")
            print_l(inst_list)
                     
def main(): 
    if(len(sys.argv) > 1):
        apk_name = sys.argv[1]
    else:
        usage()
        sys.exit(1)

    methods = init(apk_name)
    scan_methods(methods)

if __name__ == "__main__":
    main()

