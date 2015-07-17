import json
from dir import Dir
from result import Result

def get_result(conf):
    # Load config file
    f = open(conf, 'r')
    conf = json.loads(f.read())
    f.close()

    d = Dir(conf)
    res = d.get_result()

    return res
