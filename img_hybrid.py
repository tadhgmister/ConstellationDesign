from plotutil import HighDimScatter
import itertools


# Example usage:
def make_hybrid():
    # Create HighDimScatter instance with 4 dimensions, a super title, and a grid
    high_dim_scatter = HighDimScatter(4, super_title="High-Dimensional Scatter Plots", grid=range(7))

    # Example data
    QAM16 = list(itertools.product([0, 2, 4, 6], repeat=2))
    QAM8 = [p for p in itertools.product([1,3,5], repeat=2) if p!=(3,3)]

    pointsA = [a+b for a,b in itertools.product(QAM16,QAM8)]
    pointsB = [b+a for a,b in itertools.product(QAM16,QAM8)]
    

    # Call scatter method to plot the data
    high_dim_scatter.scatter(pointsA, marker='o', label='A')
    high_dim_scatter.scatter(pointsB, marker='x', label='B')

    # Save the figure
    return high_dim_scatter
if __name__ == "__main__":
    x = make_hybrid()
    x.save()
