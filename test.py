#!/usr/bin/env python3


from Circ.Matrix import HiddenSum

def test():
    c = HiddenSum(N=3,k=1)

    for i in range(1,8):
        print("{},{}".format(i,i))
        print("{}".format(c.ring(i,i)))

test()
