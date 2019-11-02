import json, sys

def json_parse_stdin():
    str_input = "".join(sys.stdin.readlines())
    objs, i = [], 0
    while i < len(str_input):
        try:
            obj, index = json.JSONDecoder().raw_decode(str_input[i:])
            objs.append(obj)
            i += index
        except:
            i += 1
    return objs