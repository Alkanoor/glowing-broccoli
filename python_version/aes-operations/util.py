import re
import base64
import hashlib
from os import listdir
from os.path import isdir, isfile, join
from Crypto.Cipher import AES

def base64_no_slash_encode(m):
    return base64.b64encode(m).replace('/','_').replace('+','-')

def base64_no_slash_decode(m):
    return base64.b64decode(m.replace('_','/').replace('-','+'))

def full_path(t):
    return t[1]+'/'+t[0]

def extend_dir(dirs,files,cur):
    to_ignore = []
    if isfile(join(full_path(cur), '.ignore')):
        ignore_file = open(join(full_path(cur), '.ignore'), 'r')
        to_ignore = [l.split('\n')[0] for l in ignore_file.readlines()]
    tmp11 = [(f,full_path(cur)) for f in listdir(full_path(cur)) if isfile(join(full_path(cur), f))]
    tmp21 = [(f,full_path(cur)) for f in listdir(full_path(cur)) if isdir(join(full_path(cur), f))]
    if len(to_ignore)>0:
        tmp12 = []
        tmp22 = []
        for t in tmp11:
            bad = False
            for r in to_ignore:
                if re.match(r,t[0]):
                    bad = True
            if not bad:
                tmp12.append(t)
        for t in tmp21:
            bad = False
            for r in to_ignore:
                if re.match(r,t[0]):
                    print(t)
                    print(r)
                    bad = True
            if not bad:
                tmp22.append(t)
        files.extend(tmp12)
        dirs.extend(tmp22)
    else:
        files.extend(tmp11)
        dirs.extend(tmp21)

class Counter:
    def reset_counter(self, v):
        self.v = v
    def current_val(self):
        return self.v

counter = Counter()

def get_current_counter():
    return counter.current_val()

def craft_key(filename):
    key = open(filename,'rb').read()
    h = hashlib.sha256()
    h.update(key)
    key = h.digest()[:AES.block_size]
    return key
