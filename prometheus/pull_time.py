#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 16:45
# @Author  : laazy
# @Site    : 
# @File    : pull_time.py
# @Software: PyCharm

import time
import sys


class TimePuller:
    begin_time = sys.maxsize
    end_time = 0
    nodes = ["2", "3", "4", "5", "6", "7"]

    def __init__(self):
        pass

    def pull_properties(self, raw_id):
        for i in self.nodes:
            with open("/home/wuchunghsuan/MR-Monitoring-Tools/output/" + raw_id + "-" + i, "r") as f:
                raw_str = f.readlines()
                self.begin_time = min(self.begin_time,self.process_properties(raw_str[0]))
                self.end_time = max(self.end_time, self.process_properties(raw_str[-1]))
        if self.begin_time == 0:
            return -1
        else:
            return 0

    @staticmethod
    def process_properties(raw_str):
        if len(raw_str) < 24:
            return 0
        raw_str = raw_str[0:23]
        left_ms = int(raw_str[20:23])
        timestamp = int(time.mktime(time.strptime(raw_str[0:19], "%Y-%m-%d %H:%M:%S"))) * 1000
        return left_ms + timestamp

    def get_start_time(self):
        return self.begin_time

    def get_finish_time(self):
        return self.end_time


if __name__ == '__main__':
    te = TimePuller()
    te.pull_properties("application_1553323617432_0105")
    print(te.begin_time)
    print(te.end_time)
