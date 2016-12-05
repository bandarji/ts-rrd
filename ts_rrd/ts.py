import requests

class TrafficServer(object):

    def __init__(self, display_name=None, url=None):
        if display_name: self.display_name = display_name
        if url: self.url = url
        self.error = ""
        self.stats_json = {}

    def pull_stats(self):
        try:
            stats = requests.get(self.url)
            if stats.status_code = 200:
                self.stats_json = stats.json
            else:
                self.error = "Error: response code not 200"
        except requests.exceptions.ConnectionError:
            self.error = "Error: unable to connect to {}".format(self.url)
        if self.error:
            return False
        else:
            return True

    def exit(self):
        if self.error:
            sys.stderr.write("{}\n".format(self.error))
        else:
            sys.stderr.write("Error: unknown\n")
        sys.exit(1)
