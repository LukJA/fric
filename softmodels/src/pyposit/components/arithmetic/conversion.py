def gen_bin_u(v: int, n: int):
    q = format(int(v), 'b')
    if len(q) < n: # sign extend
        q = "0"*(n-len(q)) + q
    if q[0] == "1":
        raise Exception("Not Unsigned")
    return q

def i_bin_u(v: str):
    return int(v, 2)

def gen_bin_s(v: int, n: int):
    if v < 0:
        q = format(int(-v), 'b')
        if len(q) < n: # extend
            q = "0"*(n-len(q)) + q
        q = twoc(q, n)
    else:
        q = format(int(v), 'b')
        if len(q) < n: # sign extend
            q = "0"*(n-len(q)) + q
    return q

def i_bin_s(q: str):
    if q[0] == "1":
        # negative
        q = twoc(q, len(q))
        return -i_bin_u(q)
    else:
        return i_bin_u(q)
    