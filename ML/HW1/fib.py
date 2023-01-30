import numpy

#Part 1
def fibRec(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fibRec(x-1) + fibRec(x-2)

def fibImp(x):
    z = 1
    last = 0
    Tlast = 1
    total = 1
    while z != x:
        total = last + Tlast
        last = Tlast
        Tlast = total
        z+=1
    return total

def fibMatrix(x):
    matrix = numpy.array([[1,1],[1,0]], dtype='object') 
    #got from geeksforgeeks how to square a matrix https://www.geeksforgeeks.org/raise-a-square-matrix-to-the-power-n-in-linear-algebra-using-numpy-in-python/
    newMat = numpy.linalg.matrix_power(matrix, x)
    return newMat[1][0]

print(fibRec(8))
print(fibImp(8))
print(fibMatrix(8))




#Part 2






#part 3
"""
The intution between the knn algorithm is that if we hav an unkown data point, if we find the most similar data point, we can assume
that the 2 of them have the same target value. For example, if boys speak about sports more and girls speak about shopping more
and we find that random person talking about baseball, we can assume that there is a higher chance that this person is a boy rather a 
girl. 

Pseudocode:
    Step 1: gather all of the training data points
    Step 2: compare how far our testing data point is relative to the previous data points
    Step 3: Sort them by the distance (manhattan, hamming, eculidian...)
    Step 4: take the k closest points and compare them to our data point. 
    Step 5: vote to see which this point is most similar to.
    Step 6: return our answer.
"""