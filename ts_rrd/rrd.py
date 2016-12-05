import os
import rrdtool

class RRD(object):

    def __init__(self, rrd_dir=None, display_name=None):
        if rrd_dir: self.rrd_dir = rrd_dir

    def write(self, stats, ts_name):
        rrd_file = "{}/{}.rrd".format(self.rrd_dir, ts_name)
        if os.path.isfile(rrd_file):
            image_file = "{}/{}.png".format(rrd_dir, ts_name)
            rrd_cmd_list = [
                image_file,
                '--imgformat', 'PNG',
                '--step', '60',
                '--end', 'now',
                '--start', 'end-1d',
                '--width=720', '--height=120',
                '--font', 'DEFAULT:6:',
                '--watermark', '{}'.format(time.strftime("%F-%R-%Z")),
                '--upper-limit', '20'
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
            # rrdtool.create() does not accept Unicode
            for i, v in enumerate(rrd_cmd_list):
                rrd_cmd_list[i] = str(v)
        rrdtool.create(rrd_cmd_list)
