def bin_invert(s: str):
    """Swap all the ones and zero in a bin string"""
    q = s
    q = q.replace("1", "A")
    q = q.replace("0", "1")
    q = q.replace("A", "0")
    return q

def twoc(s: str, n: int) -> str:
    # Flip all bits
    q = bin_invert(s)
    ## Add 1 and ignore overflow
    q = format(int(q, 2) + int("1", 2), 'b')
    if len(q) < n:
        q = "0"*(n-len(q)) + q
    return q[-n:]
