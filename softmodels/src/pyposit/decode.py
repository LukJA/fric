def count_regime(p: str):
    """Count the number of regime bits in a posit string."""
    if p[0] not in p[1:]:
        return len(p) - 1
    return p[1:].index(p[0])

def split_posit(p: str, *, es: int = 2) -> tuple[int, int, int, int]:
    """Split a posit string p into sign, regime, exponent, and fraction."""
    len_regime = count_regime(p)
    sign = 1 if p[0] == 0 else -1

    len_exp = min(len(p) - 1 - len_regime, es)

    if len_exp == 0:
        reg = int(p[1:], base=2)
        exp = 0
        frac = 0
    elif len_exp < es:
        reg = int(p[1:len_regime+1], base=2)
        exp = int(p[-len_exp:] + "0" * (es - len_exp), base=2)
        frac = 0
    else:
        reg = int(p[1:len_regime+1], base=2)
        exp = int(p[len_regime+1:len_regime+1+es], base=2)
        frac = int(p[len_regime+1+es:], base=2)
    
    return ( sign, reg, exp, frac )