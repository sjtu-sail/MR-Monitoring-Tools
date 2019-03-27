import json

import DataPulling
import pull_time
from draw import Drawer
import os
import numpy as np
import sys

TYPE_LIST = ["{}/{}_cpu", "{}/{}_net", "{}/{}_disk_read", "{}/{}_disk_write"]
JSON_DIR = "mytask"
PIC_DIR = "pic"


def my_sum(data):
    ret = np.zeros(len(data[0]["value"]))
    for d in data:
        ret += np.array(d["value"])
    return ret.tolist()


def merge_data(nodes, title, labels):
    assert len(nodes) > 0
    return {
        # "title": nodes[0]["title"],
        "title": title,
        "interval": nodes[0]["interval"],
        "data": [{
            "name": labels[i],
            "value": my_sum(node["data"])
        } for i, node in enumerate(nodes)]
    }


def run(title, need_pulling=True):
    if need_pulling:
        time_puller = pull_time.TimePuller()
        assert time_puller.pull_properties(title) != -1
        DataPulling.pulling(title, time_puller.get_start_time() / 1000 , time_puller.get_finish_time() / 1000)
    drawer = Drawer()

    for dl in TYPE_LIST:
        drawer.load_data(dl.format(JSON_DIR, title))
        drawer.draw_line_graph(dl.format(PIC_DIR, title))


def prepare_env():
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    if not os.path.exists(PIC_DIR):
        os.makedirs(PIC_DIR)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage:  main.py application id")
    prepare_env()
    run(title=sys.argv[1], need_pulling=True)

    # with open("example.json") as f:
    #     obj = json.loads(f.read())
    # obj2 = obj.copy()
    # print(merge_data([obj, obj2], 'title', ['hhhh', 'llll']))
