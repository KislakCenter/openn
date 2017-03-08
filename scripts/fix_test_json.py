#!/usr/bin/env python

import sys
import json

def main():

    # for line in sys.stdin:
    #     sys.stderr.write("DEBUG: got line: " + line)
    #     sys.stdout.write(line)
    in_json = ''
    for line in sys.stdin:
        in_json += line

    out_data = []
    data = json.loads(in_json)
    for item in data:
        if "model" in item and item["model"] != "openn.repository":
            out_data.append(item)
    print json.dumps(out_data)
    # with open(filename) as file_obj:
    #     data = json.load(file_obj)
    #     for item in data:
    #         if "model" in item and item["model"] != "openn.repository":
    #             out_data.append(item)

    # print data
    # print json.dumps(out_data)
    # with open(filename, 'w') as outfile:
    #     json.dump(data, outfile, encoding="utf-8", ensure_ascii=False)
    return 0

if __name__ == '__main__':
    main()
