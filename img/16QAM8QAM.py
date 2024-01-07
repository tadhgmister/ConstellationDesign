import itertools
import matplotlib.pyplot as plt
from sys import stdout


# Create meshgrid using itertools.product
QAM16points = list(itertools.product([0, 2, 4, 6], repeat=2))

# Unpack coordinates into separate X and Y lists
X, Y = zip(*QAM16points)

QAM8points = [ (x,y) for (x,y) in itertools.product([1,3,5],repeat=2) if (x,y)!=(3,3)]

# Create scatter plot
plt.scatter(*zip(*QAM16points), marker='o', label='16QAM')
plt.scatter(*zip(*QAM8points), marker='o', label='8QAM')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('16QAM and rectangular 8QAM')
#plt.legend()


# Show grid on all integer values
plt.grid(True)
plt.xticks(range(7))
plt.yticks(range(7))

# Set equal axis scaling and limits
plt.axis('equal')
plt.axis([-1, 7, -1, 7])

# Save the figure directly to stdout
plt.savefig(stdout.buffer, format='png')
