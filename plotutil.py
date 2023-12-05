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
            ax.set_title(f'Scatter Plot - Dimensions {2 * idx + 1} and {2 * idx + 2}')
            ax.axis('equal')
            ax.axis([min(grid) - 1, max(grid) + 1] * 2)
            ax.grid(True)
            ax.set_xticks(grid)
            ax.set_yticks(grid)

    def scatter(self, points, **kwargs):
        coord_vectors = list(zip(*points))

        # Loop over subplots and call scatter on each one
        for idx, ax in enumerate(self.axs):
            ax.scatter(coord_vectors[2 * idx], coord_vectors[2 * idx + 1], **kwargs)

    def save(self):
        self.fig.savefig(stdout.buffer, format='png')

