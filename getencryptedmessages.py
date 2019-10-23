#!/usr/bin/python

import re
import json
import argparse
import os


def get_json_messageblocks(filename):
    with open(filename, "r") as f:
        content = [i for i in f.read().splitlines() if re.search(r'\{"messageKey"', i) is not None]

    scrubbed = [re.sub(r'(!|#|")$', '', i) for i in content]
    scrubbed = [re.sub(r'\\', '', i) for i in scrubbed]
    json_data = [json.loads(i) for i in scrubbed]

    return json_data


def remove_duplicate_messages(json_list):
    message_sigs = list(set([i["messageSig"] for i in json_list]))
    result = list()
    for i in json_list:
        if i['messageSig'] in message_sigs:
            result.append(i)
            message_sigs.remove(i['messageSig'])
    return result


parser = argparse.ArgumentParser()

parser.add_argument("filename", help="name of file to extract messages from", type=str)
parser.add_argument("-o", "--old-filename", help="old filename. This will compare the two files and extract any messages that are different between the two", type=str)
parser.add_argument("--output", help="output file name", type=str)
args = parser.parse_args()

if not os.path.isfile(args.filename):
    print("filename does not exist")
    exit(1)

if args.old_filename is not None and not os.path.isfile(args.old_filename):
    print("old_filename does not exist")
    exit(1)



new_json = remove_duplicate_messages(get_json_messageblocks(args.filename))

if args.old_filename is not None:
    old_json = remove_duplicate_messages(get_json_messageblocks(args.old_filename))
    new_message_sigs = set([i["messageSig"] for i in new_json])
    old_message_sigs = set([i["messageSig"] for i in old_json])
    difference = new_message_sigs - old_message_sigs
    new_messages = [i for i in new_json if i["messageSig"] in difference]
else:
    new_messages = new_json

if args.output is None:
    for i in new_messages:
        print(json.dumps(i))
else:
    with open(args.output, "w") as f:
        json.dump(new_messages, f)

