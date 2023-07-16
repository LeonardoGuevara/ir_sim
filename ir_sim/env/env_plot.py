import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class EnvPlot:

    def __init__(self, subplot=False, **kwargs) -> None:

        if not subplot:
            self.fig, self.ax = plt.subplots()

        else:
            self.fig, self.ax, self.sub_ax_list = self.world.sub_world_plot()



        self.init_plot(**kwargs)
    

    def init_plot(self, no_axis=False, **kwargs):
        
        self.ax.set_aspect('equal') 
        self.ax.set_xlim(self.world.x_range) 
        self.ax.set_ylim(self.world.y_range)
        
        self.ax.set_xlabel("x [m]")
        self.ax.set_ylabel("y [m]")

        self.draw_components(self.ax, mode='static', **kwargs)

        if no_axis: plt.axis('off')


    def sub_world_plot(self):

        # row: default 3
        # colum: default 3
        # number: number of subplot
        # scheme: default; 
        #         custom; 
        # custom_layout: coordinate of the main and sub axises (custom scheme)
        #       - [[x_min, x_max, y_min, y_max], [x_min, x_max, y_min, y_max]]
        #   
        number = self.sub_plot_kwargs.get('number', 0)
        row = self.sub_plot_kwargs.get('row', 3)
        column = self.sub_plot_kwargs.get('column', 3)
        layout = self.sub_plot_kwargs.get('layout', 'default')
        custom_layout = self.sub_plot_kwargs.get('custom_layout', [])

        fig = plt.figure(constrained_layout=True)
        sub_ax_list = []

        assert number < row * column

        if number == 0:
            ax = fig.add_subplot(111)
        else:
            gs = GridSpec(row, column, figure=fig)

            if layout == 'default':
                coordinate = [[0, row, 0, column-1], [0, 1, 2, 3], [1, 2, 2, 3], [2, 3, 2, 3]]
            elif layout == 'custom':
                coordinate = custom_layout

            for n in range(number): 
                c = coordinate[n]

                if n == 0:
                    ax = fig.add_subplot(gs[c[0]:c[1], c[2]:c[3]])
                else:
                    sub_ax = fig.add_subplot(gs[c[0]:c[1], c[2]:c[3]])
                    self.init_sub_plot(sub_ax)
                    sub_ax_list.append(sub_ax) 

        return fig, ax, sub_ax_list

        


    
