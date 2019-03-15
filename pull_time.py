#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:36
# @Author  : laazy
# @Site    : 
# @File    : pull_time.py
# @Software: PyCharm

import os


class TimePuller:
    properties = {}

    def __init__(self, app_id):
        raw_str = self.pull_properties(app_id)
        self.process_properties(raw_str)
        pass

    @staticmethod
    def pull_properties(raw_id):
        with os.popen("/home/wuchunghsuan/hadoop-2.8.5/bin/yarn application -status " + raw_id, "r") as f:
            return f.read()

    def process_properties(self, raw_str):
        s = raw_str.split("\n\t")
        for i in s:
            i = i.strip()
            i = i.split(":")
            self.properties[i[0].strip()] = i[1].strip()

    def get_property(self, name):
        return self.properties[name]

    def get_start_time(self):
        return self.get_property("Start-Time")

    def get_finish_time(self):
        return self.get_property("Finish-Time")


if __name__ == '__main__':
    te = TimePuller("application_1552279621115_0003")
    ans = te.properties
    print(ans)
