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

    def __init__(self):
        pass

    def pull_properties(self, raw_id):
        with os.popen("/home/wuchunghsuan/hadoop-2.8.5/bin/yarn application -status " + raw_id, "r") as f:
            raw_str = f.read()
        self.properties = self.process_properties(raw_str)
        if self.properties == {}:
            return -1
        else:
            return 0

    @staticmethod
    def process_properties(raw_str):
        s = raw_str.split("\n\t")
        if len(s) < 3:
            return {}
        ret_pro = {}
        for i in s:
            i = i.strip()
            i = i.split(":")
            ret_pro[i[0].strip()] = i[1].strip()
        return ret_pro

    def get_property(self, name):
        return self.properties[name]

    def get_start_time(self):
        return int(self.get_property("Start-Time"))

    def get_finish_time(self):
        return int(self.get_property("Finish-Time"))


if __name__ == '__main__':
    te = TimePuller()
    te.pull_properties("application_1552279621115_0003")
    ans = te.properties
    print(ans)
