#On remplace tous les fichiers de dates differentes par rapport au fichiers pulled
#argv[1] = dest_dir
#argv[2] = base_dir

import re
import sys
import base64
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from list_target_files import *


if len(sys.argv)<2:
    print("[-] Usage "+sys.argv[0]+" <source dir>")

src = sys.argv[1]

print(list_target_files(src))
exit()

dirs = []
files = []

extend_dir(dirs,files,('.',src))

for i in range(len(dirs)):
    extend_dir(dirs,files,dirs[i])

print(dirs)
print(files)

key = open('key','r').readlines()[0].split('\n')[0]
for f in files:
    try:
        enc = base64.b64decode(full_path(f))
        iv = enc[:16]
        cipher = AES.new(key, AES.MODE_CTR, iv)
        cur_file = unpad(cipher.decrypt(enc[16:]))
    except Exception as e:
        print("[-] Error during AES deciphering, please verify the key ("+str(e.args[0])+")")
        print("[-] Aborting ...")
        exit()
    if isfile(cur_file):
        cur_date = 1 #get date(cur_file)
        pulled_date = 1 #get date(f)
        replace = False
        if cur_date != f:
            if cur_date > pulled_date:
                print("[+] Warning, current date is superior as pulled one, are you sure that you want replace the file ? [N/y]")
                i = raw_input()
                if i == 'y':
                    replace = True
            else:
                replace = True
    if replace:
        content_file = open(full_path(f),'rb').read()
        try:
            enc = base64.b64decode(content_file)
            iv = enc[:16]
            cipher = AES.new(key, AES.MODE_CTR, iv)
            content = unpad(cipher.decrypt(enc[16:]))
        except Exception as e:
            print("[-] Error during AES deciphering of file "+full_path(f)+", please verify the key ("+str(e.args[0])+")")
            print("[-] Aborting ...")
            exit()
        try:
            g = open(cur_file,'wb+')
            g.write(content)
            print("[+] File replaced")
        except Exception as e:
            print("[-] Error during file replacement of "+cur_file+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
