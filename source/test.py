import numpy as np

def func(x):
    # b = x[:]
    # x[0]=x[0]/2
    for i,m in enumerate(x):
        m=m/2
if __name__ == '__main__':

    a = [np.array([1,2,3]),np.array([4,5])]
    print(a)
    func(a)
    print(a)
    b = [22,55,66]
