#!/usr/bin/env python3


from Circ.Matrix import HiddenSum

def test():
    c = HiddenSum(N=3,k=1)

    for i in range(8):
        for j in range(8):
            #if i == 5 and j == 5:
                #c.binary_to_int(c.ring(i,j))
            print("{}".format(c.binary_to_int(c.ring(i,j))), end=' ')
        print()
    #print(c.Bex)
    # print()
    # for i in range(8):
    #     for j in range(8):
    #         #if i == 5 and j == 5:
    #             #c.binary_to_int(c.ring(i,j))
    #         print("{}".format(c.xor(i,j)), end=' ')
    #     print()

test()
