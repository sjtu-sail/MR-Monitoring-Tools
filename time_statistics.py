#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 14:29
# @Author  : laazy
# @Site    : 
# @File    : time_statistics.py
# @Software: PyCharm
import log_deal2


class TimeStatistic:
    def __init__(self):
        pass

    def get_time(self, log):
        ans = {}
        for job in log:
            ans[job] = self.get_time_by_job(log, job)
        return ans

    @staticmethod
    def get_time_by_job(log, job):
        ans = {"map": 0, "shuffle": 0, "reduce": 0}
        for node in log[job]:
            for task in log[job][node]:
                for status in ans:
                    if log[job][node][task].get(status) is None:
                        continue
                    time = log[job][node][task][status]
                    ans[status] += (time[1] - time[0])
        return ans


if __name__ == '__main__':
    logs = log_deal2.LogDealer()
    statistic = TimeStatistic()
    logs.load_dirs()
    t = statistic.get_time(logs.get_output())
    print(t)
