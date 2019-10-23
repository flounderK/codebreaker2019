import base64
import logging
import hashlib
from datetime import datetime
import re
import string
from Crypto.Util import Padding
from Crypto.Cipher import PKCS1_v1_5
import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import json
from cryptography.hazmat.primitives import keywrap, padding
from cryptography.hazmat.backends import default_backend
import argparse
import os
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("json", help="json file to get messages from")
parser.add_argument("-f", "--fingerprints",
                    help="instead of message contents, print"
                    " public key fingerprints matched with users",
                    action="store_true", default=False)
args = parser.parse_args()

public_key_fingerprint = 'bhr9+Yya+1LoLhSMbizF7R8Tpq3+E4Jlp8LdcfDkoq4='
with open("robertopublickey", "r") as f:
    pubkey = RSA.import_key(f.read())

with open("robertoprivatekey", "r") as f:
    privkey = RSA.importKey(f.read())

ciph = PKCS1_v1_5.new(privkey)


if not os.path.isfile(args.json):
    print(f"{args.json} is not a file")
    exit(1)

with open(args.json, "r") as f:
    try:
        all_messages = json.load(f)
    except:
        print("File does not appear to be in json format")
        exit(1)

if isinstance(all_messages, dict):
    all_messages = [all_messages]

public_fingerprints = defaultdict(list)
for message_json in all_messages:
    messageKey = message_json['messageKey']
    message = message_json['message']
    for v in [v for k, v in messageKey.items() if k == public_key_fingerprint]:
        v = base64.b64decode(v)

        message_key_decrypted = ciph.decrypt(v, "FAIL")

        aes = AES.new(message_key_decrypted,
                      AES.MODE_CBC,
                      iv=base64.b64decode(message['iv']))
        decrypted_msg = aes.decrypt(
            base64.b64decode(message['msg'])).decode().strip()
        decrypted_msg = ''.join(filter(lambda x: x in string.printable,
                                       decrypted_msg))
        if args.fingerprints is False:
            print(decrypted_msg)
        else:
            decrypted_msg = json.loads(decrypted_msg)
            for name, pkfs in filter(lambda a: a[0] != 'body',
                                     decrypted_msg.items()):
                public_fingerprints[name].extend(pkfs)


if args.fingerprints is True:
    public_fingerprints = dict(public_fingerprints)
    for k, v in public_fingerprints.items():
        public_fingerprints[k] = list(set(v))
    print(public_fingerprints)

