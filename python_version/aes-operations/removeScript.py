import re
import os
import sys
import base64
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from list_target_files import *


if len(sys.argv)<3:
    print("[-] Usage "+sys.argv[0]+" <source dir> <key filename> [temporary dst cpy (../tmp by default)]")

print("[!!] Warning, this operation is reserved when you know what you do (because local files that do not match remote ones will be deleted)")
print("[!!] Are you sure you want to commit and erase files that do not match remote files ? [N/y]")
i = raw_input()
if i != 'y':
    print("[-] Aborted")
    exit()

src = sys.argv[1]
dst = os.getcwd()
key = craft_key(sys.argv[2])
if len(sys.argv)>=4:
    tmp_dst = sys.argv[3]
else:
    tmp_dst = '../tmp'
os.rename(dst, tmp_dst)

files = list_target_files(src,key)

for target,last_modif_target,ciphered,last_modif_in_ciphered in files:
    try:
        enc = base64.b64decode(open(ciphered,'rb').read())
        ctr = enc[AES.block_size:2*AES.block_size]
        counter.reset_counter(ctr)
        cipher = AES.new(key, AES.MODE_CTR, counter=get_current_counter)
        file_content = cipher.decrypt(enc[3*AES.block_size:])
    except Exception as e:
        print("[-] Error during AES deciphering, please verify the key ("+str(e.args[0])+")")
        print("[-] Aborting ...")
        exit()

    existing = True
    if isfile(target): # Should not happen here as directory has been moved to tmp
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
        tmp = split_target[0]
        i = 1
        while isdir(tmp) and i+1<len(split_target):
            tmp += "/"+split_target[i]
            i += 1
        replace = True
        existing = False
        if not isdir(tmp):
            try:
                os.makedirs('/'.join(split_target[:-1]))
            except:
                print("[!] Seems there is a problem with "+ciphered)
                print("[?] Do you want to delete the file ? (be sure of what you're doing)")
                i = raw_input()
                if i == 'y':
                    os.remove(ciphered)
                    replace = False
                    print("[-] File "+ciphered+" deleted")

    if replace:
        try:
            g = open(target,'wb+')
            g.write(file_content)
            if existing:
                print("[+] File "+target+" replaced")
            else:
                print("[+] File "+target+" created")
            g.close()
            os.utime(target, (last_modif_in_ciphered, last_modif_in_ciphered))
        except Exception as e:
            print("[-] Error during file replacement of "+target+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
