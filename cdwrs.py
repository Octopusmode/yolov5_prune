from math import sqrt
a = [121, 144, 19, 161, 19, 144, 19, 11]  
b = [121, 14641, 20736, 361, 25921, 361, 20736, 361]

def comp(array1, array2):
    array1.sort()
    array2.sort()
    for i, v in enumerate(array1):
        array1[i] = array1[i]**2
    return array1 == array2

comp(a, b)