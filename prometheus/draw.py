import json
from pyecharts import Line, Bar


class Drawer:
    def __init__(self, obj=None):
        """
        Crate the instance
        :param obj: either the json filename or an object.
                    If leaving blank, you can always revoke
                    @func{load_data} to load the data
        """
        self.title = None
        self.interval = None
        self.interval_str = None
        self.data = None
        if obj is not None:
            self.load_data(obj)

    def load_data(self, obj):
        if type(obj) == str:
            if len(obj) <= 5 or obj[-5:] != '.json':
                obj += '.json'
            with open(obj) as f:
                obj = json.loads(f.read())
        self.title = obj["title"]
        self.interval = obj["interval"]
        # cast interval items to string for correctness
        self.interval_str = list(map(lambda x: str(x), self.interval))
        self.data = obj["data"]

    def draw_line_graph(self, dist=None, is_stack=False):
        """
        draw line graph
        :param is_stack: draw stack graph or not
        :param dist: where you want to save the graph. If leaving blank,
                     it will generate a html file containing the graph
        """
        line = Line(self.title, title_pos="center", is_animation=True)
        for d in self.data:
            assert len(self.interval_str) == len(d["value"])
            line.add(d["name"], self.interval_str, d["value"],
                     is_xaxislabel_align=True,
                     legend_orient='vertical',
                     legend_pos='80%',
                     line_width=3,
                     is_smooth=False,
                     is_stack=is_stack,
                     is_fill=is_stack,
                     area_opacity=0.4,
                     is_symbol_show=False)
        self.save_pic(line, dist)

    def draw_bar_graph(self, dist=None):
        bar = Bar(self.title, title_pos="center", is_animation=False)
        for d in self.data:
            assert len(self.interval_str) == len(d["value"])
            bar.add(d["name"], self.interval_str, d["value"],
                    is_xaxislabel_align=True,
                    legend_orient='vertical',
                    legend_pos='80%')
        self.save_pic(bar, dist)

    @staticmethod
    def save_pic(graph, dist):
        if dist is None or dist == '':
            graph.render()
        else:
            if len(dist) <= 4 or dist[-4:] != '.png':
                print("Warning: PNG is the only supported format")
                dist += '.png'
            graph.render(dist)


if __name__ == '__main__':
    drawer = Drawer("mytask/123_cpu.json")
    drawer.draw_line_graph()
