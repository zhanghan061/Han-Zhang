#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    domain = words[len(words)-4]
    suffix='nasa.gov'
    response_bytes = int(words[len(words)-1])
    if domain.endswith(suffix):
        print '%s\t%s' % ('total bandwidth', response_bytes)
    

