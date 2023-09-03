from math import isinf

def float_to_posit(f: float, *, n: int = 32, es: int = 2) -> str:
    n_bits = n
    useed = pow(2, pow(2, es))

    y = abs(f)
    e = pow(2, es - 1)

    # quickly check these two unique cases first
    if f == 0:
        return '0' * n_bits
    if isinf(f):
        return '1' + '0' * (n_bits - 1)
    
    # if our number doesn't meet the special cases, solve iteratively
    if f >= 0:  # northeast quadrant
        p = 1
        i = 2

        while y >= useed and i < n_bits:
            p = 2*p + 1
            y /= useed
            i += 1

        p *= 2
        i += 1

    else:  # southeast quadrant
        p = 0
        i = 1

        while y < 1 and i <= n_bits:
            y *= useed
            i += 1

        if i >= n_bits:
            p = 2
        elif i == n_bits + 1:
            p = 1
        else:
            i += 1

    # extract exponent bits
    while e > 0.5 and i <= n_bits:
        p *= 2
        
def posit_to_float(p: str, *, n: int = 32, es: int = 2) -> float:
    """Generate float from posit string."""
    return 0.0  # FIXME
