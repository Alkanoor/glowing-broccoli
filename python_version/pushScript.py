#On remplace tous les fichiers de dates differentes par rapport au fichiers pulled
#argv[1] = dest_dir
#argv[2] = base_dir

import re
import sys
import hashlib
import binascii
from util import *
from Crypto import Random
from Crypto.Cipher import AES


force_replace = False

if len(sys.argv)<3:
    print("[-] Usage "+sys.argv[0]+" <source dir> <destination dir> [force replacement]")
elif len(sys.argv)>3:
    force_replace = (sys.argv[3]=='1')

src = sys.argv[1]
dst = sys.argv[2]

dirs = []
files = []

extend_dir(dirs,files,('.',src))

for i in range(len(dirs)):
    extend_dir(dirs,files,dirs[i])

print(dirs)
print(files)


key = open('key','r').read()
h = hashlib.sha256()
h.update(key)
key = h.digest()[:AES.block_size]
for f in files:
    try:
        raw = full_path(f)
        iv = Random.new().read(AES.block_size)
        ctr = Random.new().read(AES.block_size)
        counter.reset_counter(ctr)
        cipher = AES.new(key, AES.MODE_CTR, iv, get_current_counter)
        enc = base64_no_slash_encode(cipher.encrypt(raw))
        iv_ctr_name_enc = iv+ctr
    except Exception as e:
        print("[-] Error during AES ciphering : "+str(e.args[0]))
        print("[-] Aborting ...")
        exit()
    if isfile(dst+"/"+enc):
        cur_date = 1 #get date(cur_file)
        pushed_date = 2 #get date(f)
        replace = False
        if not force_replace:
            if cur_date != f:
                if cur_date < pushed_date:
                    print("[+] Warning, current date is inferior as pushed one, are you sure that you want replace the file ? [N/y]")
                    i = raw_input()
                    if i == 'y':
                        replace = True
                else:
                    replace = True
    else:
        replace = True
    if replace or force_replace:
        content_file = open(full_path(f),'rb').read()
        try:
            g = open(dst+"/"+enc,'wb+')
        except Exception as e:
            print("[-] Error during file replacement of "+dst+"/"+enc+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
        try:
            raw = content_file
            iv = Random.new().read(AES.block_size)
            ctr = Random.new().read(AES.block_size)
            counter.reset_counter(ctr)
            cipher = AES.new(key, AES.MODE_CTR, iv, get_current_counter)
            print(binascii.hexlify(iv+ctr))
            enc = iv+ctr+cipher.encrypt(raw)
        except Exception as e:
            print("[-] Error during AES ciphering of file "+full_path(f)+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
        try:
            print(binascii.hexlify(iv_ctr_name_enc))
            g.write(base64.b64encode(iv_ctr_name_enc+enc))
            print("[+] File replaced")
        except Exception as e:
            print("[-] Error during file replacement of "+dst+"/"+enc+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
