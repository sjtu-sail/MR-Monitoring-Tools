import numpy as np
import matplotlib as mpl

mpl.use('Agg')
from matplotlib.pyplot import xlabel, ylabel, title, grid, plot, savefig
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from log_deal_skew import LogDealer
import sys
import getopt
import time
import os

OUT_DIR = './output_pic'

class ExecutedDraw:
    waves_color = ["blue"]
    map_line_styles = ['-', '--', '-.', ':']
    agg =[]
    node_agg = np.zeros(4,dtype=long)


    def draw(self,loger):
        max_key = 0
        for obj in loger.logs:
            if  obj["key"] > max_key:
                max_key = obj["key"]
        self.agg =np.zeros(max_key+1,dtype= long)
        xlabel("Slots")
        ylabel("TotalSize")
        title("Test")
        for obj in loger.logs:
            self.agg[obj["key"]] +=  obj["size"]
        self.agg= sorted(self.agg, reverse=True)
        plt.bar(range(len(self.agg)), self.agg, fc='r')
        plt.show()
    def draw_node(self,loger):
        xlabel("Nodes")
        ylabel("TotalSize")
        title("Test")
        for node,list in loger.node2log.items():
            i = node
            for obj in list:
                self.node_agg[i] += obj["size"]
        self.node_agg = sorted(self.node_agg,reverse = True)
        plt.bar(range(len(self.node_agg)), self.node_agg, fc='r')
        plt.show()





    def save(self,name):
        path = OUT_DIR
        if not (os.path.exists(path)):
            os.makedirs(path)
        savefig(path + '/' + str(int(time.time()))+"_"+name + ".png")



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: python draw_skew.py ids_file draw_type"
        exit(1)
    app_ids= sys.argv[1]
    draw_type= int(sys.argv[2])
    app_name = ""
    file_ids = open(app_ids,'r')
    for id in file_ids:
        app_name = id
	
    log = LogDealer()
    app_name = app_name.strip()
    log.get_files("./output_skew/",app_name)
    #print log.logs
    img = ExecutedDraw()

    file_sub = ""
    if draw_type == 1:
        img.draw(log)
        file_sub="skew_tasks"
    else:
        img.draw_node(log)
        file_sub = "skew_nodes"
    img.save(file_sub)
