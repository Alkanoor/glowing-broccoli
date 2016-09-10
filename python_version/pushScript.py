import re
import sys
import hashlib
import binascii
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from list_target_files import *


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

i = 0
while i<len(dirs):
    extend_dir(dirs,files,dirs[i])
    i += 1

cur_encoded = list_target_files(dst)
dict_cur_encoded = {}
dict_to_delete_if_replace = {}

for u,v,w,x in cur_encoded:
    if dict_to_delete_if_replace.get(u) is not None:
        print("Removing file "+w+" because corresponding unciphered file is already here")
        os.remove(w)
    else:
        dict_cur_encoded[u] = (v,x)
        dict_to_delete_if_replace[u] = w

key = craft_key('key')

for f in files:
    try:
        raw = full_path(f)
        iv = Random.new().read(AES.block_size)
        ctr = Random.new().read(AES.block_size)
        iv_ctr_name_enc = iv+ctr
        counter.reset_counter(ctr)
        cipher = AES.new(key, AES.MODE_CTR, iv, get_current_counter)

        enc = base64_no_slash_encode(cipher.encrypt(raw))

        date = format(int(os.path.getmtime(raw)),'x')
        date = '0'*(AES.block_size*2-len(date))+date

        assert(len(date)//2==AES.block_size)
        date_enc = cipher.encrypt(binascii.unhexlify(date))
        assert(len(date_enc)==AES.block_size)
    except Exception as e:
        print("[-] Error during AES ciphering : "+str(e.args[0]))
        print("[-] Aborting ...")
        exit()

    existing = True
    if dict_cur_encoded.get(full_path(f)) is not None:
        cur_date,pushed_date = dict_cur_encoded[full_path(f)]
        replace = False
        if not force_replace:
            if cur_date != pushed_date:
                if cur_date < pushed_date:
                    print("[+] Warning, current date is inferior as pushed one, are you sure that you want replace the file ? [N/y]")
                    i = raw_input()
                    if i == 'y':
                        replace = True
                else:
                    replace = True
    else:
        replace = True
        existing = False

    if replace or force_replace:
        content_file = open(full_path(f),'rb').read()
        try:
            g = open(dst+"/"+enc,'wb+')
        except Exception as e:
            print("[-] Error during file creation of "+dst+"/"+enc+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
        try:
            raw = content_file
            iv = Random.new().read(AES.block_size)
            ctr = Random.new().read(AES.block_size)
            counter.reset_counter(ctr)
            cipher = AES.new(key, AES.MODE_CTR, iv, get_current_counter)
            enc_content = iv+ctr+date_enc+cipher.encrypt(raw)
        except Exception as e:
            print("[-] Error during AES ciphering of file "+full_path(f)+" : "+str(e.args[0]))
            print("[-] Aborting ...")
            exit()
        try:
            g.write(base64.b64encode(iv_ctr_name_enc+enc_content))
            g.close()
            if existing:
                os.remove(dict_to_delete_if_replace[full_path(f)])
                print("[+] File "+dict_to_delete_if_replace[full_path(f)]+" deleted and recreated at "+(dst+"/"+enc)+" for original file "+full_path(f))
            else:
                print("[+] File "+(dst+"/"+enc)+" created for original file "+full_path(f))
        except Exception as e:
            print("[-] Error during file creation of "+dst+"/"+enc+" : "+str(e.args[0])+" for original file "+full_path(f))
            print("[-] Aborting ...")
            exit()
