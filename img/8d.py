from plotutil import HighDimScatter
import itertools
bases = [
    0b11110000,
    0b10011100,
    0b00111010,
    0b00001111,
]
bases = [
    0b10000111,
    0b01001011,
    0b00101101,
    0b00011110,
    ]

QAMpoints = list(itertools.product([0,1], repeat=8))

fig = HighDimScatter(8, "test", {i/2:f"{i}/2" for i in range(4)})

for bias_bits in reversed(range(2**len(bases))):
    bias = 0
    for pos in range(len(bases)):
        if bias_bits & (2**pos):
            bias ^= bases[pos]
    bias = tuple(map(int, f"{bias:08b}"))
    [a,b,c,d] = map(int, f"{bias_bits:04b}")
    XXX = [tuple(p+q/2 for p,q in zip(qam,bias)) for qam in QAMpoints]
    #raise Exception(len(list(zip(*XXX))))
    fig.scatter(XXX,
                marker=  'o*sD'[a*2+b],
                markersize=6*(c*2+d+a*0.5+2),
                markeredgecolor = ["red","blue","orange","green"][c*2+d],
                
                markerfacecolor="none")


fig.save()
