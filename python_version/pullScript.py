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
files = list_target_files(src)

key = craft_key('key')

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
                print("[+] Warning, current date is superior as pulled one, are you sure you want to replace the file ? (and possibly lose data) [N/y]")
                i = raw_input()
                if i == 'y':
                    replace = True
            else:
                replace = True
    else:
        tmp = target.split('/')
        os.makedirs('/'.join(tmp[:-1]))
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
