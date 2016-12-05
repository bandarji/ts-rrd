import sys

class Arguments(object):

    def __init__(self):
        pass

    def validate_command_line(self):
        if len(sys.argv) == 4:
            if sys.argv[3][0:4] != 'http':
                sys.stderr.write("URL must start with application 'http'\n")
                sys.exit(1)
        else:
            sys.stderr.write("Usage: ts-rrd <rrd_dir> <display_name> <url>\n")
            sys.exit(1)
        args = {
            "rrd_dir": sys.argv[1],
            "display_name": sys.argv[2],
            "url": sys.argv[3]
        }
        return args
