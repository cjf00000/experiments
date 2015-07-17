import sys, os, json
from result import Result
import datetime
from utils import touch
import utils

class Dir:
    def arg_id(self, arg):
        result = self.name
        for k, v in arg:
            result = result + '-' + k + '-' + str(v)
        return result

    def write_time(self, t): 
        f = open('time-used', 'w')
        f.write(str(t))
        f.close()

    def read_time(self):
        f = open('time-used', 'r')
        t = float(f.read())
        f.close()
        return t

    def __init__(self, conf):
        self.conf = conf
        self.name = conf["name"]

        if not os.path.exists(self.name):
            os.mkdir(self.name)

        os.chdir(self.name)

        if not os.path.exists('time-used'):
            self.write_time(0)

        self.start_time = datetime.datetime.now()
        self.time_used = self.read_time()

        self.result = Result(conf)

        self.refresh()

    def read(self, arg):
        newresult = {}

        f = open(self.arg_id(arg), 'r')
        for line in f.readlines():
            line = line.strip().split()
            if len(line) % 2 == 1 or len(line) < 2:
                # Fail
                utils.fail(self.arg_id(arg))
                f.close()
                return

            new_key = {k : v for k, v in arg}
            # parse line
            for i in xrange(0, len(line)-2, 2):
                i_name = line[i]
                i_value = float(line[i+1])

                new_key[i_name] = i_value

            new_key["name"] = line[-2]
            newresult[utils.dict2tuple(new_key)] = float(line[-1])

        # Merge result with newresult
        for k in newresult.keys():
            self.result[k] = newresult[k]

        f.close()

    def refresh(self):
        # Load data
        self.finished_tasks = 0
        for arg in self.result.args():
            if utils.finished(self.arg_id(arg)):
                if not utils.failed(self.arg_id(arg)):
                    self.read(arg)
                self.finished_tasks += 1

        self.total_tasks = len(self.result.args())
        t = datetime.datetime.now()
        td = t - self.start_time
        self.start_time = t

        self.time_used += td.seconds * 1e6 + td.microseconds 
        self.write_time(self.time_used)

    def write_status(self, cr = True):
        percentage = self.finished_tasks * 100 / self.total_tasks
        content = '%s: %d/%d (%d%%)' \
            % (self.name, self.finished_tasks, self.total_tasks, percentage)

        s = self.time_used / 1e6
        m = int(s/60) % 60
        h = int(s/3600) % 24
        d = int(s/86400)
        s = s % 60

        if d==0:
            content += ' Time: %02d:%02d:%02d' % (h, m, s)
        else:
            content += ' Time: %d d %02d:%02d:%02d' % (d, h, m, s)

        if cr:
            content = '\r' + content

        sys.stdout.write(content)
        sys.stdout.flush()

    def start(self, arg):
        f = open(self.arg_id(arg) + '.todo', 'w')
        content = json.dumps(arg)
        f.write(content)
        f.close()

    def get_result(self):
        return self.result

if __name__ == '__main__':
    touch('test')
