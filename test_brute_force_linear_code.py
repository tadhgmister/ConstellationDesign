

# number of dimensions (elements) of the code
N = 16
# min distance from each element to each other element
K = 4

STARTING_WORDS = [
    (0,)*N,
    (1,)*K + (0,)*(N-K),

    #((1,)* 8 + (0,)* 8)*2,
    #((1,)* 4 + (0,)* 4)*4
    ]
print(*STARTING_WORDS,sep="\n",end="\n\n")

import itertools
viable_but_not_equadistant = 0
too_close = 0
for word in itertools.product((1,0), repeat=N):
    lengths = [sum(a^b for a,b in zip(base,word)) for base in STARTING_WORDS ]
    if any(a<K for a in lengths):
        too_close += 1
        continue
    elif all(a==K for a in lengths):
        print(word)
    else:
        viable_but_not_equadistant+=1
        continue

print("too far:",viable_but_not_equadistant)
print("too close:", too_close)
