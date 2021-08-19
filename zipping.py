from zipfile import ZipFile
 
 
def zipping(filename, filepath, zipfilename):
    print(f'[*] zip file<{zipfilename}> {filename} as path {filepath} ')
    with ZipFile(zipfilename, 'w') as z:
        z.write(filename, filepath)
        print(z.namelist())
 
if __name__ == "__main__":
    import sys
    zipfilename = 'zip.zip'
    if len(sys.argv) < 2:
        print('[*] ZIPPING.py <filename> <filepath> [zipfileName:default zip.zip]')
        quit()
    if len(sys.argv) > 3:
        zipfilename = sys.argv[3]
 
    zipping(sys.argv[1], sys.argv[2], zipfilename)

