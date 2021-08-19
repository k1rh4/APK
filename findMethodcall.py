from androguard.misc import AnalyzeAPK
from bs4 import BeautifulSoup
import sys
import glob 

target_methods = ["System;->load","System;->loadLibrary","Runtime;->exec","ProcessBuilder;->start",
                  "BaseDexClassLoader;-><init>","DexClassLoader;-><init>","PathClassLoader;-><init>"]

def what_function_calls(dx, target_method:str)->set:
    ret = set()
    classes = dx.get_classes()
    for _class in classes:
        methods = _class.get_methods()
        for _method in methods:
            for target in target_method:
                if target in str(_method):
                    for class_name, method_name, num in _method.get_xref_from():
                        ret.add((("<<"+target+">>\n"), method_name))
                    
    if ret :
        print(f'[+]targets is called by functions below({len(ret)})')
        for target_name, method_name in ret:
            print(f'{target_name}{str(method_name)}')

            source_code = method_name.get_method().source()
            print(f'\t{source_code}')
            print(f'------------------------------------------------------------------------------')
    else: 
        print(f'[-]targets is not called')
    
    return ret


def search_what_function_calls(path:str, target_methods:list):    
    print(f'[*]{path}')
    a, d, dx = AnalyzeAPK(path)
    what_function_calls(dx, target_methods)


def main(file_name):
    search_what_function_calls( file_name, target_methods )


if __name__ =="__main__":
    #main(sys.argv[1]);

    
    files = glob.glob("./systemAPPS/*")
    for file_name in files:
        print("[*] Analysis : %s " %file_name)
        main(file_name)
