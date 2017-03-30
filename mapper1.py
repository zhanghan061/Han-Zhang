#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    response_bytes = words[len(words)-1]
    if '/Jul/' in words[3]:
        print '%s\t%s' % ('total bandwidth', response_bytes)
    

