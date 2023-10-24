import typing as t

def listToBinary(digits : t.List[int]) -> int: 
    return sum(c << i for i, c in enumerate(digits))

FLOAT_MAX = 3.402823466E+38 