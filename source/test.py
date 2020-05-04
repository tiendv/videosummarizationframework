
def  add(a,b):
    return a+b

def  mul(a,b,c):
    return a*b*c

def test(func,*argv):
    print(func(*argv))

test(add,5,7)
test(mul,4,5,6)
