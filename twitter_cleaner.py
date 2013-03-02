""" twitter_cleaner.py - Combine and clean up Twitter archive.

Cleans up all the json files in your downloaded Twitter archive and combines
them into one big json for easy storage and/or uploading to Splunk Storm.

Splunk Storm: http://www.splunkstorm.com.

Note: as of 2013-03-01, you should us the "JSON (auto timestamp)" sourcetype
when uploading the output file to Splunk Storm.
"""

__author__ = "Ed Hunsinger"
__copyright__ = "Copyright 2013"
__email__ = "edrabbit@edrabbit.com"

import json
import os
import sys


def process_file(file_path):
    '''Process a file_path and return a json string'''
    fp = open(file_path, 'r')
    lines = fp.readlines()
    lines[0] = ''  # kill the first line stuff that's not needed
    jd = json.loads(''.join(lines))

    output = json.dumps(jd, indent=2)
    output = output[4:-1]  # Trim away some []s
    output = output.replace('\n  ', '\n')  # Storm hates two spaces before {

    return output

if __name__ == "__main__":
    print ('====Twitter Cleaner====\n %s\n %s\n %s\n'
           % (__author__, __email__, __copyright__))
    if len(sys.argv) < 2:
        print ('Usage: %s [path_to_twitter_archive_dir] [output_file]'
               % os.path.basename(sys.argv[0]))
        print ('\npath_to_twitter_archive_dir should be the directory you '
               'extracted your downloaded archive to, with the data subfolder')
        exit(1)
    else:
        tweets_dir = sys.argv[1]
        if not os.path.isdir(tweets_dir):
            print 'Invalid directory provided'
            exit(1)
        if not os.path.isdir(os.path.join(tweets_dir, 'data')):
            print 'Unable to find data directory'
            exit(1)

        output_file_path = sys.argv[2]
        output = ''

    tweets_data_dir = os.path.join(tweets_dir, 'data', 'js', 'tweets')
    for f in os.listdir(tweets_data_dir):
        if '.js' in f:
            print 'Processing %s' % f
            output = output + process_file(os.path.join(tweets_data_dir, f))

    of = open(output_file_path, 'w')
    of.write(output)
    of.close()
    print 'Tweets written to %s' % output_file_path
