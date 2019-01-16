import os
import sys
class LogDealer:
    def __init__(self):
        self.logs = []
        self.node2log={}

    def get_logs(self,filename):
        node_logs = []
        node2logs =[]
        with open(filename, "r") as f:
            for s in f.readlines():
                ans,type = self.line_process(s)
                if  type == 0:
                    node_logs.append(ans)
                else:
                    node2logs.append(ans)
        self.logs = self.logs+node_logs
        return  node_logs,node2logs
    def get_files(self,dirs,appname):
        for i, j, k in os.walk(dirs):
            for file in k:
                if file.find(appname) >=0:
                    res ,node_log= self.get_logs(os.path.join(i, file))
                    flist = file.split('-')
                    node =int(flist[-1])-1
                    self.node2log[node] = node_log

    def line_process(self, s):
        ans ={}
        type = 0
        s = s.split("OPS:")[-1]
        if s.find("reduce input")>=0:
            s = s.split("reduce input")[-1].strip().strip('[').strip(']')
            list = s.split(',')
            ans ={"mapID": int(list[0]),"size":int(list[1])}
            type =1
        else:
            s= s.strip().strip('[').strip(']')
            lists = s.split(',')
            ans = {"key": int(lists[0]),"offset": int(lists[1]),"size":int(lists[2])}
        return ans,type

