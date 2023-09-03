def bin_add_u(a: str, b: str, n: int):
    """Add two unsigned binary values and extend to n"""
    q = format(int(a, 2) + int(b, 2), 'b')
    if len(q) < n:
        q = "0"*(n-len(q)) + q
    dprint.debug(f"{a}+{b}={q}")
    return q

def bin_add_s(a: str, b: str):
    """Add two binary values"""
    if len(a) != len(b):
        raise Exception("Signed Addition Mismatch")
    a_s = a[0]
    b_s = b[0]
    q = format(int(a, 2) + int(b, 2), 'b')
    if len(q) < len(a): # sign extend
        q = "0"*(len(a)-len(q)) + q
    dprint.debug(f"{a}+{b}={q}")

    if a_s == "0" and b_s == "0" and q[0] == "1":
        raise Exception("Pos Overflow")
    if a_s == "1" and b_s == "1" and q[0] == "0":
        raise Exception("Neg Overflow")
    return q[-len(a):]

def bin_sub_u(a: str, b: str, n: int):
    """Sub b from a unsigned """
    q = format(int(a, 2) - int(b, 2), 'b')
    if len(q) < n:
        q = "0"*(n-len(q)) + q
    dprint.debug(f"{a}-{b}={q}")
    return q

def bin_sub_s(a: str, b: str):
    """Sub two binary values"""
    if len(a) != len(b):
        raise Exception("Signed Addition Mismatch")
    b =  twoc(b, len(a))
    return bin_add_s(a, b)

