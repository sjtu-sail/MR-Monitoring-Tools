# import matplotlib.pypot as plt
import numpy as np
import matplotlib as mpl

mpl.use('Agg')
from matplotlib.pyplot import xlabel, ylabel, title, grid, plot, savefig
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from log_deal2 import LogDealer
import sys
import getopt
import time
import os

OUT_DIR = './output_pic'


class ExecutedDraw:
    waves_color = ["blue"]
    map_line_styles = ['-', '--', '-.', ':']
    map_id_num = {}
    count = 0
    def map_draw(self, slot, dots):
        if dots is None:
            return
        np_dots = np.array(dots)
        slots = np_dots.copy()
        slots[:] = slot
        self.l_map, = plot(np_dots, slots, lw=1, linestyle=self.map_line_styles[1], color=self.waves_color[0],
                           marker='|')

    def reduce_draw(self, slot, dots):
        if dots == None:
            return
        np_dots = np.array(dots)
        slots = np_dots.copy()
        slots[:] = slot
        self.l_reduce, = plot(np_dots, slots, lw=1, linestyle='-', color='black', marker='|')

    def shuffle_draw(self, slot, dots):
        if dots == None:
            return
        slots = [i for i in dots]
        slot = slot + 0.5
        for i in range(len(slots)):
            slots[i] = slot
        self.l_shuffle, = plot(dots, slots, lw=1, linestyle='-', color='brown', marker='|')

    def draw(self, containers, jobid):
        for job, node_list in containers.items():
            if job == jobid:
                for node, task_list in node_list.items():
                    for taskid, phase_list in task_list.items():
                        if taskid in self.map_id_num:
                            tasknum = self.map_id_num[taskid]
                        else:
                            tasknum = self.count
                            self.map_id_num[taskid] = tasknum
                            self.count += 1
                        self.map_draw(tasknum, phase_list["map"])
                        self.shuffle_draw(tasknum, phase_list["shuffle"])
                        self.reduce_draw(tasknum, phase_list["reduce"])

    def save(self,maxtime):

        plt.legend([self.l_map, self.l_reduce, self.l_shuffle], ['map', 'reduce', 'shuffle'], loc='center',
                   bbox_to_anchor=(0.5, 1.105), ncol=3)
        base = (self.count / 10)-(self.count/10) %10
        if   self.count<=100:
            base = 10
        # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator((self.count / 10)-(self.count/10) %10))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base))
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator((maxtime / 10)-(maxtime/10)%10))
        # plt.figure(figsize=(10, 8))
        # plt.subplots_adjust(left=0.09, right=1, wspace=0.25, hspace=0.25, bottom=0.13, top=0.91)
        path = OUT_DIR
        if not (os.path.exists(path)):
            os.makedirs(path)
        plt.savefig(path + '/' + str(int(time.time())) + ".png")
        # plt.show()


def main():


    if len(sys.argv) != 2:
        print "error: missing parameter: job_id"
        exit(1)
    job_text = sys.argv[1]

    max_time=0
    log_data = LogDealer()
    draw_test = ExecutedDraw()
    file_job = open(job_text, 'r')
    for job_id in file_job:
        job_id = job_id.strip()
        # print job_id
        draw_data,max_time = log_data.process(job_id)
        draw_test.draw(draw_data, job_id)
    draw_test.save(max_time)
    file_job.close()



# draw_data = log_data.process(job_id)
# draw_test.draw(draw_data, job_id)

if __name__ == '__main__':
    main()
