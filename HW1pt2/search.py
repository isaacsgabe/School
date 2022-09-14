#search

import state
import frontier
total = 0

push = 0
pop = 0
depth = 0

def search(n):
    global push
    global pop
    global depth
    s=state.create(n)
    f=frontier.create(s)
    while not frontier.is_empty(f):
        s=frontier.remove(f)
        if state.is_target(s):
            push += f[2]
            pop += f[3]
            depth += len(s[1])
            return [s, f[1]]
        ns=state.get_next(s)
        for i in ns:
            frontier.insert(f,i)
    return 0

# for i in range(10000):
#     x = search(3)
#     total += x[1]
# total/=10000
# print(total)

for x in range(100):
    print(x)
    search(4)
push /= 100
pop/=100
depth/=100
print("that amount pushed on the frontier is " + str(push))
print("that amount popped off the frontier is " + str(pop))
print("the total depth is: " + str(depth))


"""
#######################################
part 2
#######################################
a) with hdistance1 unweighted

4x4 with hdistance1 regular
    that amount pushed on the frontier is 44314.13
        that amount popped off the frontier is 21062.86
        the total depth is: 16.73


############################################


4x4 with hdistance2 regular
    that amount pushed on the frontier is 2408.14
    that amount popped off the frontier is 1199.71
    the total depth is: 16.48

####################
2*hdistance1.... weighted


4x4
    that amount pushed on the frontier is 14362.15
    that amount popped off the frontier is 6790.93
    the total depth is: 16.9

####################
2*hdistance2.... weighted

4x4
    that amount pushed on the frontier is 1717.59
    that amount popped off the frontier is 855.2
    the total depth is: 17.78




"""




