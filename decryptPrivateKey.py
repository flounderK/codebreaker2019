import hashlib
import string
from Crypto.Cipher import AES
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("database", help="Client database to extract private key from")
parser.add_argument("-o", "--output", help="File to dump extracted private key into")
args = parser.parse_args()


if not os.path.isfile(args.database):
    print(f"{args.database} is not a valid file")
    exit(1)

try:
    conn = sqlite3.connect("clientDB.db")
    c = conn.execute('select * from Clients')
    # put data in a usable format
    data = {k: v for k, v in zip(map(lambda x: x[0], c.description),
                                 [i for i in c][0])}
    c.close()
    conn.close()
except:
    pass

client_pin = b'412270'
key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=client_pin,
            salt=data['checkpin'],
            iterations=0x2710,
            dklen=32)

cip = AES.new(key=key, mode=AES.MODE_ECB)
privkey = cip.decrypt(data['privkey']).decode()
privkey = ''.join([i for i in privkey if i in string.printable[:-2]])

if args.output is not None:
    with open(args.output, "w") as f:
        f.write(privkey)
else:
    print(privkey)

