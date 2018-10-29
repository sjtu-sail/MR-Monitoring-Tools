import os

'''
    output structure:
    {
        node1:{
            job_1:{
                task_1:{
                    "map":[
                        begin_time, end_time
                    ],
                    "shuffle":[...],   //if it is lack of properties, its value is `None` 
                    "reduce":[...]
                },
                task_2:{}, ...
            },
            job_2:{}, ...
        },
        node2:{}, ...
    }
'''
phase_def = {
    "phase_name": ["map", "reduce", "shuffle"],
}


class LogDealer:
    def __init__(self):
        self.source_file = "./output/"
        self.logs = {}
        self.output = None

    # load file from directory
    def load_files(self, job_id):
        for node_id in ("2", "3", "4"):
            self.load_file(node_id, job_id)

    # load content from file
    def load_file(self, node_id, job_id):
        self.output = None
        # job_id, node = self.create_node_job(os.path.basename(job_id))
        filename = self.source_file + job_id + "-" + node_id
        self.logs[node_id] = {job_id: {}}

        node_logs = []
        cnt = 0
        with open(filename, "r") as f:
            for s in f.readlines():
                node_logs.append(self.line_process(s))
                cnt += 1
        for i, j in node_logs:
            if self.logs[node_id][job_id].get(i) is None:
                self.logs[node_id][job_id][i] = []
            self.logs[node_id][job_id][i].append(j)
        return cnt

    # # create node and job if not exist
    # def create_node_job(self, name):
    #     tmp = name.split("-")
    #     node = tmp[0]
    #     job_id = tmp[1]
    #     if self.logs.get(node) is None:
    #         self.logs[node] = {job_id: {}}
    #         return node, job_id
    #     if self.logs[node].get(job_id) is None:
    #         self.logs[node][job_id] = {}
    #     return node, job_id

    # get output and cache it
    def get_output(self):
        if self.output is not None:
            return self.output
        ans = {}
        for node in self.logs:
            ans[node] = {}
            for job in self.logs[node]:
                ans[node][job] = {}
                for task in self.logs[node][job]:
                    ans[node][job][task] = self.get_phase(self.logs[node][job][task])
        self.output = ans
        return ans

    # change format of phase
    @staticmethod
    def get_phase(phase):
        ans = {}
        for k in phase_def["phase_name"]:
            ans[k] = {}
        for i in phase:
            ans[i["phase"]][i["status"]] =str(int(i["timestamp"])/1000)
        for i in ans:
            if ans[i] == {}:
                ans[i] = None
            else:
                ans[i] =[ans[i]["start"], ans[i]["stop"]]
        return ans

    # process log file line
    @staticmethod
    def line_process(s):
        s = s.split(" ")[-1].split("-")
        ans = {"timestamp": s[1].strip(), "phase": s[3].strip(), "status": s[4].strip()}
        return s[2], ans

    def process(self, job_id):
        self.load_files(job_id)
        return self.get_output()


if __name__ == '__main__':
    log = LogDealer()
    print log.process("1540438986149_0010")



