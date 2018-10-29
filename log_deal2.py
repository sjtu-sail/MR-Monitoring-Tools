import os
import sys

'''
    output structure:
    {
        job_1:{
            node_1:{
                task_1:{
                    "map":[
                        begin_time, end_time
                    ],
                    "shuffle":[...],   //if it is lack of properties, its value is `None` 
                    "reduce":[...]
                },
                task_2:{}, ...
            },
            node_2:{}, ...
        },
        job_2:{}, ...
    }
'''
log_def = {
    "phase_name": ["map", "reduce", "shuffle"],
    "node_name": ["1", "2", "3", "4"],
    "log_dir": "./output/"
}


class LogDealer:
    def __init__(self):
        self.logs = {}
        self.output = None
        self.min = sys.maxsize

    def load_job(self, job_id, log_dir=log_def["log_dir"]):
        """
        load job by job id
        :param job_id:
        :param log_dir:
        :return:
        """
        for node_id in log_def["node_name"]:
            self.load_job_from_file(node_id, job_id.strip(), log_dir)

    def load_dirs(self, dirs=log_def["log_dir"]):
        for i, j, k in os.walk(dirs):
            for file in k:
                self.load_file(os.path.join(i, file))

    # load content from file
    def load_file(self, filename):
        tmp = os.path.basename(filename).split("-")
        node_id = tmp[1]
        job_id = tmp[0]
        self.load_content(filename, node_id, job_id)
        # filename = self.source_file + job_id + "-" + node_id
        # self.logs[node_id] = {job_id: {}}

    def load_job_from_file(self, node_id, job_id, log_dir):
        """
        load job from file from log_dir which was denoted by job_id and node_id

        :param node_id:
        :param job_id:
        :param log_dir:
        :return:
        """
        self.load_content(log_dir + job_id + "-" + node_id, node_id, job_id)

    def load_content(self, filename, node_id, job_id):
        node_logs = []
        cnt = 0
        self.output = None
        self.create_job_node(node_id, job_id)
        with open(filename, "r") as f:
            for s in f.readlines():
                node_logs.append(self.line_process(s))
                cnt += 1
        for i, j in node_logs:
            if self.logs[job_id][node_id].get(i) is None:
                self.logs[job_id][node_id][i] = []
            self.logs[job_id][node_id][i].append(j)
        return cnt

    # create node and job if not exist
    def create_job_node(self, node_id, job_id):
        """
        create job and node if they are not existed
        :param node_id:
        :param job_id:
        :return:
        """
        if self.logs.get(job_id) is None:
            self.logs[job_id] = {node_id: {}}
            return
        if self.logs[job_id].get(node_id) is None:
            self.logs[job_id][node_id] = {}
        return

        # get output and cache it

    def get_output(self):
        """
        when load file, the cache of output will be eraser, so be careful to load at once
        get output form loaded log
        :return: formatted and processed log
        """
        if self.output is not None:
            return self.output
        ans = {}
        for job in self.logs:
            ans[job] = {}
            for node in self.logs[job]:
                ans[job][node] = {}
                for task in self.logs[job][node]:
                    ans[job][node][task] = self.get_phase(self.logs[job][node][task])
        self.output = ans
        return ans

    # change format of phase
    def get_phase(self, phase):
        """
        get each phase from a task
        :param phase:
        :return:
        """
        ans = {}
        for k in log_def["phase_name"]:
            ans[k] = {}
        for i in phase:
            ans[i["phase"]][i["status"]] = (i["timestamp"] - self.min) / 1000
        for i in ans:
            if ans[i] == {}:
                ans[i] = None
            else:
                ans[i] = [ans[i]["start"], ans[i]["stop"]]
        return ans

    # process log file line
    def line_process(self, s):
        s = s.split(" ")[-1].split("-")
        ans = {"timestamp": int(s[1].strip()), "phase": s[3].strip(), "status": s[4].strip()}
        self.min = min(self.min, ans["timestamp"])
        return s[2], ans

    def process(self, job_id):
        self.load_job(job_id)
        return self.get_output()


if __name__ == '__main__':
    log = LogDealer()
    log.load_dirs()
    t = log.get_output()
    print(t)
    # print
    # log.process("1540438986149_0010")
