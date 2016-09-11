import re
import sys
import base64
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from list_target_files import *


if len(sys.argv)<3:
    print("[-] Usage "+sys.argv[0]+" <source dir> <key filename>")

src = sys.argv[1]
key = craft_key(sys.argv[2])

files = list_target_files(src,key)

for target,last_modif_target,ciphered,last_modif_in_ciphered in files:
    try:
        enc = base64.b64decode(open(ciphered,'rb').read())
        iv = enc[2*AES.block_size:3*AES.block_size]
        ctr = enc[3*AES.block_size:4*AES.block_size]
        counter.reset_counter(ctr)
        cipher = AES.new(key, AES.MODE_CTR, iv, get_current_counter)
        file_content = cipher.decrypt(enc[5*AES.block_size:])
    except Exception as e:
        print("[-] Error during AES deciphering, please verify the key ("+str(e.args[0])+")")
        print("[-] Aborting ...")
        exit()

    existing = True
    if isfile(target):
        replace = False
        if last_modif_target != last_modif_in_ciphered:
            if last_modif_target > last_modif_in_ciphered:
                print("[+] Warning, current date of "+target+" is superior as pulled one, are you sure you want to replace the file ? (and possibly lose data) [N/y]")
                i = raw_input()
                if i == 'y':
                    replace = True
            else:
                replace = True
    else:
        split_target = target.split('/')
        print(split_target)
        tmp = split_target[0]
        i = 1
        while isdir(tmp) and i+1<len(split_target):
            tmp += "/"+split_target[i]
            i += 1
        if not isdir(tmp):
            os.makedirs('/'.join(split_target[:-1]))
        replace = True
        existing = False

    if replace:
        try:
            g = open(target,'wb+')
            g.write(file_content)
            if existing:
                print("[+] File "+target+" replaced")
            else:
                print("[+] File "+target+" created")
        except Exception as e:
            print("[-] Error during file replacement of "+target+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
