import os
import sys
class LogDealer:
    def __init__(self):
        self.logs = []
        self.node2log={}

    def get_logs(self,filename):
        node_logs = []


        with open(filename, "r") as f:
            for s in f.readlines():
                node_logs.append(self.line_process(s))
        self.logs = self.logs+node_logs
        return  node_logs
    def get_files(self,dirs):
        for i, j, k in os.walk(dirs):
            for file in k:
                res = self.get_logs(os.path.join(i, file))
                flist = file.split('-')
                node =int(flist[-1])-1
                self.node2log[node] = res

        # process log file line
    def line_process(self, s):
        s = s.split("OPS:")[-1].strip().strip('[').strip(']')
        lists = s.split(',')
        ans = {"key": int(lists[0]),"offset": int(lists[1]),"size":int(lists[2])}
        return ans

if __name__ == '__main__':
    log = LogDealer()
    log.get_files("output")
    print (log.logs)