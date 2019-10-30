import hashlib
import string
from Crypto.Cipher import AES
import sqlite3
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("database", help="Client database to extract private key from")
parser.add_argument("-p", "--pin", help="Known client pin", type=str)
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

if args.pin is None:
    checkpin = data['checkpin']
    for i in [str(i).rjust(6, '0').encode() for i in range(1000000)]:
        if hashlib.sha256(i).digest() == checkpin:
            client_pin = i
            break
else:
    client_pin = args.pin.encode()

# client_pin = b'412270'

key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=client_pin,
            salt=data['checkpin'],
            iterations=0x2710,
            dklen=32)

cip = AES.new(key=key, mode=AES.MODE_ECB)
privkey = cip.decrypt(data['privkey']).decode()
privkey = ''.join(filter(lambda x: x in string.printable, privkey))

csecret = cip.decrypt(data['csecret']).decode()
csecret = ''.join(filter(lambda x: x in string.printable, csecret))
print(f"cid: {data['cid']}\n")
print(f"Pin: {client_pin.decode()}\n")
print(f"Client Secret: {csecret}\n")
print(privkey)
print(data['pubkey'])

