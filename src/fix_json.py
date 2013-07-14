import json
import sys

o = json.load(sys.stdin)

for e in o:
    e['pk'] = None
    print json.dumps(e, indent=4)
    print ","
