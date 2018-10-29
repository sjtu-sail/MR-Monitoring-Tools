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
OUT_DIR='./output_pic'

class ExecutedDraw:
    waves_color = ["blue"]
    map_line_styles = ['-', '--', '-.', ':']
    map_id_num = {}
    count = 0

    def __init__(self):
        xlabel("Time(in seconds)")
        ylabel("Task slots")
        title("Test")
        grid(True, linestyle='-.')

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
        # plt.xticks(np.linspace(-1, 1, 5))
        # plt.yticks(np.linspace(-1, 1, 5))
        # plt.legend([self.l_map, self.l_reduce, self.l_shuffle], ['map', 'reduce', 'shuffle'], loc='upper center')

    # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(20))
    # plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(500))
    # savefig(str(jobid) + ".png")

    # show()

    def save(self):

        plt.legend([self.l_map, self.l_reduce, self.l_shuffle], ['map', 'reduce', 'shuffle'], loc='center',
                   bbox_to_anchor=(0.5, 1.05), ncol=3)
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(20))
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))
        path = OUT_DIR
        if not (os.path.exists(path)):
 	    os.makedirs(path)
        savefig(path+'/'+ str(int(time.time())) + ".png")


def main():
    # filename = ''
    # job_id = ''
    # opts, args = getopt.getopt(sys.argv[1:], '-h-v', ['help', 'version'])
    # for opt_name, opt_value in opts:
    #     if opt_name in ('-h', '--help'):
    #         print("[*] Help info")
    #         exit()
    #     if opt_name in ('-v', '--version'):
    #         print("[*] Version is 0.01 ")
    #         exit()

    if len(sys.argv) != 2:
        print "error: missing parameter: job_id"
        exit(1)
    job_text = sys.argv[1]

    log_data = LogDealer()
    draw_test = ExecutedDraw()
    file_job = open(job_text, 'r')
    for job_id in file_job:
        job_id = job_id.strip()
	#print job_id
        draw_data = log_data.process(job_id)
        draw_test.draw(draw_data, job_id)
    file_job.close()
    draw_test.save()


# draw_data = log_data.process(job_id)
# draw_test.draw(draw_data, job_id)

if __name__ == '__main__':
    main()
