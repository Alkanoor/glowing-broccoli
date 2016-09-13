import os
import hashlib
import binascii
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from os.path import isfile


def list_target_files(target_dir,key):
    ret = []
    dirs = []
    files = []

    extend_dir(dirs,files,('.',target_dir))

    i = 0
    while i<len(dirs):
        extend_dir(dirs,files,dirs[i])
        i += 1

    for f in files:
        enc_content = open(full_path(f),'rb').read()
        try:
            enc = base64.b64decode(enc_content)
            ctr1 = enc[:AES.block_size]
            ctr2 = enc[AES.block_size:2*AES.block_size]
            read_date_enc = enc[2*AES.block_size:3*AES.block_size]
            counter.reset_counter(ctr1)
            cipher = AES.new(key, AES.MODE_CTR, counter=get_current_counter)
            filename = cipher.decrypt(base64_no_slash_decode(f[0]))
            read_date = int(binascii.hexlify(cipher.decrypt(read_date_enc)),16)
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

        non_ascii = 0
        for i in range(len(filename)):
            if ord(filename[i])<32 or ord(filename[i])>127:
                non_ascii += 1
        if non_ascii > len(filename)//3:
            print("[+] It is possible filename "+filename+" has been wrongly deciphered, please verify the key")
            print("[+] Do you want to delete the problematic file ? (do that only if you know what it means) [N/y]")
            i = raw_input()
            if i == 'y':
                os.remove(full_path(f))
                print("[-] File "+full_path(f)+" deleted")
                print("")
                continue
            else:
                print("")

        try:
            if isfile(filename):
                ret.append((filename,int(os.path.getmtime(filename)),full_path(f),read_date))
            else:
                ret.append((filename,-1,full_path(f),read_date))
        except:
            pass

    return ret
