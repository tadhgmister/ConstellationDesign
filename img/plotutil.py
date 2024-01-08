import matplotlib.pyplot as plt
from sys import stdout

class HighDimScatter:
    def __init__(self, num_dimensions, super_title, grid, figsize=5):
        if num_dimensions % 2 != 0:
            raise ValueError("Number of dimensions must be even.")
        
        self.num_dimensions = num_dimensions
        self.fig, self.axs = plt.subplots(1, num_dimensions // 2, figsize=(figsize*num_dimensions//2, figsize))

        # Set super title for the entire figure
        self.fig.suptitle(super_title)

        # Default grid to None if not provided
        if grid is None:
            grid = []

        # Loop over subplots to set properties
        for idx, ax in enumerate(self.axs):
            ax.set_xlabel(f'Dimension {2 * idx + 1}')
            ax.set_ylabel(f'Dimension {2 * idx + 2}')
            #ax.set_title(f'Dim {2 * idx + 1} and {2 * idx + 2}')
            ax.axis('equal')
            ax.axis([min(grid)-0.5, max(grid)+0.5] * 2)
            #ax.margins(1)
            ax.grid(True)
            if isinstance(grid, dict):
                ax.set_xticks(list(grid.keys()), list(grid.values()))
                ax.set_yticks(list(grid.keys()), list(grid.values()))
            else:
                ax.set_xticks(grid)
                ax.set_yticks(grid)

    def scatter(self, points, **kwargs):
        kwargs.setdefault("marker", "o")
        coord_vectors = list(zip(*points))
        assert len(coord_vectors) == self.num_dimensions, "scattering {} dimensions".format(len(coord_vectors))
        # Loop over subplots and call scatter on each one
        for idx, ax in enumerate(self.axs):
            ax.plot(coord_vectors[2 * idx], coord_vectors[2 * idx + 1], linestyle="", **kwargs)

    def save(self):
        self.fig.savefig(stdout.buffer, format='png')

