import os
import hashlib
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from os.path import isfile


def list_target_files(target_dir):
    ret = []
    dirs = []
    files = []

    extend_dir(dirs,files,('.',target_dir))

    for i in range(len(dirs)):
        extend_dir(dirs,files,dirs[i])

    key = open('key','r').read()
    h = hashlib.sha256()
    h.update(key)
    key = h.digest()[:AES.block_size]
    for f in files:
        enc_content = open(full_path(f),'rb').read()
        try:
            enc = base64.b64decode(enc_content)
            iv1 = enc[:AES.block_size]
            ctr1 = enc[AES.block_size:2*AES.block_size]
            iv2 = enc[2*AES.block_size:3*AES.block_size]
            ctr2 = enc[3*AES.block_size:4*AES.block_size]
            counter.reset_counter(ctr1)
            cipher = AES.new(key, AES.MODE_CTR, iv1, get_current_counter)
            filename = cipher.decrypt(base64_no_slash_decode(f[0]))
        except Exception as e:
            print("[-] Error during AES deciphering of file "+full_path(f)+", please verify the key ("+str(e.args[0])+")")
            print("[+] It is possible to delete the file and continue process, but data may be lost. Do that only if you are sure of what you're doing!")
            print("[+] Do you want to delete the problematic file ? [N/y]")
            i = raw_input()
            if i == 'y':
                os.remove(full_path(f))
                print("[-] File "+full_path(f)+" deleted")
                print("")
                continue
            else:
                print("[-] Aborting ...")
                exit()

        print(filename)
        if isfile(filename):
            ret.append((filename,int(os.path.getmtime(filename))))
        else:
            ret.append((filename,-1))

    return ret
