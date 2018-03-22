import re
import sys
import hashlib
import binascii
from util import *
from Crypto import Random
from Crypto.Cipher import AES
from list_target_files import *


if len(sys.argv)<4:
    print("[-] Usage "+sys.argv[0]+" <source dir> <destination dir> <key filename>")

src = sys.argv[1]
dst = sys.argv[2]
key = craft_key(sys.argv[3])

dirs = []
files = []

extend_dir(dirs,files,('.',src))

i = 0
while i<len(dirs):
    extend_dir(dirs,files,dirs[i])
    i += 1

cur_encoded = map(lambda x: x[0], list_target_files(dst,key))

something = False
for f in files:
    if os.path.join(f[1], f[0]) not in cur_encoded:
        print("New file "+os.path.join(f[1], f[0])+" will be pushed")
        something = True

fullpaths = map(lambda x: os.path.join(x[1], x[0]), files)

for f in cur_encoded:
    if f not in fullpaths:
        print("Non existing file "+f+" will be pulled.")
        something = True

if not something:
    print("Nothing to push or pull.")
