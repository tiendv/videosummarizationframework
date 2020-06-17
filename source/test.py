import numpy as np

c = np.empty(0)
a = np.array([1,2,3])
b = np.array([5,6,7,8,9,10])
d = np.array([11,12])


c = np.hstack((c,a))
c = np.hstack((c,b))
c = np.hstack((c,d))

print(c)
