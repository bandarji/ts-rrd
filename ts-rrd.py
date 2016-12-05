#!/usr/bin/python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

import ts_rrd

def main():
    args = ts_rrd.args.validate_command_line()
    ts = ts_rrd.TrafficServer(**args)
    if not ts.pull_stats(): ts.exit()
    rrd = ts_rrd.RRD(**args)
    rrd.write(ts.stats_json, ts.display_name)


if __name__ == '__main__':
    main()
#
