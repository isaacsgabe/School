#search

import state
import frontier

push = 0
pop = 0
depth = 0

def search(n):
    global push
    global pop
    global depth
    s=state.create(n)
    # print(s)
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        f[5] = f[5]+1
        if state.is_target(s):
            push += f[4]
            pop += f[5]
            depth += f[1]
            return [s, f[1]]
        ns=state.get_next(s)
        #print(ns)
        for i in ns:
            frontier.insert(f,i)
            f[4] = f[4]+1
    return 0


for x in range(3):
    search(4)
push /= 3
pop/=3
depth/=3

print(str(depth))
print(str(push))
print(str(pop))

# 2x2 (ran 100x)
# the depth is 1.75
# the number of states added was 7.34
# the number of states removed was 6.75

# 3x3 (ran 100x)
# the depth is 6.26
# the number of states added was 1440.97
# the number of states removed was 830.65

# 4x4 (ran 1x because after that it took to long)
# the depth is 15
# the number of states added was 742892
# the number of states removed was 348658




