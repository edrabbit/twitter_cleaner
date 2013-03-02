""" twitter_cleaner.py - Combine and clean up Twitter archive.

Cleans up all the json files in your downloaded Twitter archive and combines
them into one big json for easy storage and/or uploading to Splunk Storm
"""

__author__ = "Ed Hunsinger"
__copyright__ = "Copyright 2013"
__email__ = "edrabbit@edrabbit.com"

import json

# TODO(ed): Make these cmdline parameters
test_file = '2007_03.js'
output_file_path = 'out_take_4.js'

fp = open(test_file, 'r')
lines = fp.readlines()
lines[0] = ''  # kill the first line stuff that's not needed
jd = json.loads(''.join(lines))

output = json.dumps(jd, indent=2)
output = output[4:-1]  # Trim away some []s
output = output.replace('\n  ','\n') # Storm doesn't like two spaces before {

of = open(output_file_path, 'w')
of.write(output)
of.close()
