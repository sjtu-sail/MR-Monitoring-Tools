import numpy as np
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
    agg = np.zeros(32,dtype=int)
    node_agg = np.zeros(4,dtype=int)


    def draw(self,loger):
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





    def save(self):
        # plt.legend([self.l_map, self.l_reduce, self.l_shuffle], ['map', 'reduce', 'shuffle'], loc='center',
        #            bbox_to_anchor=(0.5, 1.105), ncol=3)
        # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator((self.count / 10) - (self.count / 10) % 10))
        # plt.gca().xaxis.set_major_locator(ticker.MultipleLocator((maxsize / 10) - (maxsize / 10) % 10))
        # plt.figure(figsize=(10, 8))
        # plt.subplots_adjust(left=0.09, right=1, wspace=0.25, hspace=0.25, bottom=0.13, top=0.91)
        # plt.show()
        path = OUT_DIR
        if not (os.path.exists(path)):
            os.makedirs(path)
        savefig(path + '/' + str(int(time.time()))+"_skew" + ".png")



if __name__ == '__main__':
    log = LogDealer()
    log.get_files("output")
    img = ExecutedDraw()

    # img.draw(log)
    img.draw_node(log)
    img.save()