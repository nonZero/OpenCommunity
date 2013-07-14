import sys

l = sys.stdin.readlines()

l.insert(0, "[\n")
l[-1] = ']'

sys.stdout.writelines(l)
