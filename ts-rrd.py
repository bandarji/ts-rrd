#!/usr/bin/python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

"""
import note:
    yum -y install rrdtool{,-devel}
    pip install --upgrade rrdtool
"""
import os.path
import requests
import rrdtool
import sys
import time

def error_and_exit(message, code):
    """ Write to STDERR and return to shell """
    sys.stderr.write("[ERROR]: {}\n".format(message))
    sys.exit(code)

def get_stats(url):
    return_error = {}
    try:
        stats = requests.get(url)
        if stats.status_code == 200:
            return stats.json()
        else:
            return_error['error'] = "Response code not 200"
    except requests.exceptions.ConnectionError:
        return_error['error'] = "requests.exceptions.ConnectionError"
    return return_error

def gen_list_of_strings(a_list):
    """ rrdtool.create() does not accept unicode """
    for i, v in enumerate(a_list):
        a_list[i] = str(v)
    return a_list

def wr_ts_rrd(rrd_dir, ts_name, stats_json):
    """ Write RRD file """
    rrd_file = "{}/{}.rrd".format(rrd_dir, ts_name)
    if os.path.isfile(rrd_file):
        image_file = "{}/{}.png".format(rrd_dir, ts_name)
        rrd_base_cmd_list = [
            '--imgformat', 'PNG',
            '--step', '60',
            '--end', 'now',
            '--start', 'end-1d',
            '--width=720', '--height=120',
            '--font', 'DEFAULT:6:',
            '--watermark', '{}'.format(time.strftime("%F-%R-%Z")),
            '--upper-limit', '20'
        ]
        rrd_cmd_list = [image_file] + rrd_base_cmd_list
        rrd_cmd_list = gen_list_of_strings(rrd_cmd_list)
        rrd_graph_cmd_list = [
        ]
    else:
        rrd_cmd_list = [
            rrd_file,
            '--step', '60',
            'DS:docs:DERIVE:120:0:U',
            'DS:cconns:DERIVE:120:0:U',
            'DS:sconns:DERIVE:120:0:U',
            'DS:currcc:GAUGE:120:0:U',
            'DS:currsc:GAUGE:120:0:U',
            'DS:currct:GAUGE:120:0:U',
            'DS:currst:GAUGE:120:0:U',
            'DS:reqsget:DERIVE:120:0:U',
            'DS:reqsput:DERIVE:120:0:U',
            'DS:reqspst:DERIVE:120:0:U',
            'DS:reqsdel:DERIVE:120:0:U',
            'DS:reqshed:DERIVE:120:0:U',
            'DS:res2xx:DERIVE:120:0:U',
            'DS:res3xx:DERIVE:120:0:U',
            'DS:res4xx:DERIVE:120:0:U',
            'DS:res5xx:DERIVE:120:0:U',
            'RRA:AVERAGE:0.5:1:10080'            
        ]
        rrd_cmd_list = gen_list_of_strings(rrd_cmd_list)
        print(rrd_cmd_list)
        exit(2)
        rrdtool.create(rrd_cmd_list)
    exit(2)             

def main():
    """ pull_ts_stats.py <rrd_dir> <display_name> <url> """
    stats_json = {}
    if len(sys.argv) == 4:
        if sys.argv[3][0:4] != 'http':
            error_and_exit("URL must start with application 'http'", 1)
        else:
            pass
    else:
        error_and_exit("Script requires name and url", 1)
    stats_json = get_stats(sys.argv[3])
    if 'error' in stats_json.keys():
        error_and_exit(stats_json['error'], 1)
    wr_ts_rrd(sys.argv[1], sys.argv[2], stats_json)

if __name__ == '__main__':
    main()
else:
    error_and_exit("Script name not __main__")
#
