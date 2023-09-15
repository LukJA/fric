from math import isinf
from pyposit.operations.logic import twoc

def float_to_posit(x: float, *, n: int = 32, es: int = 2) -> str:
    """Generate posit string from float."""
    # quickly check these two unique cases first
    if x == 0.0:
        return '0' * n
    if isinf(x):
        return '1' + '0' * (n - 1)

    ## grab sign and store
    if x < 0:
        sign = -1
        x *= -1
    else:
        sign = 1
    
    useed = 2**(2**es)
    ## first divide by useed or multiply by useed until it is in the 
    ## interval [1, useed).
    r = 1
    if x < 1:
        r = 0
        while(x < 1):
            x = x*useed
            r = r - 1
    elif x >= useed:
        r = 1
        while(x >= useed):
            x = x/useed
            r = r + 1

    ## next divide by 2 or multiply by 2 until it is in the 
    ## interval [1, 2).
    e = 0
    if x < 1:
        while(x < 1):
            x = x*2
            e = e - 1
    elif x >= 2:
        while(x >= 2):
            x = x/2
            e = e + 1

    ## sign and regime
    posstr = "0" #if sign == 1 else "1" ## wait till end for sign conversion
    posstr += r*"1"+"0" if r > 0 else -1*r*"0"+"1"

    ## exponent - bin string
    e = format(e, 'b')
    if len(e) < es:
        e = "0"*(es - len(e)) + e
    posstr += e

    if len(posstr) >= n:
        posstr = posstr[:n]
    else:
        ## append fraction
        ## iteratively encode the fraction (we can just keep going until we run out of precision)
        ## TODO p.s. im not sure this actually follows the correct rounding spec, like the adder does
        x -= 1
        index = -1
        while (len(posstr) < n):
            if x >= 2**(index):
                posstr += "1"
                x -= 2**(index)
            else:
                posstr += "0"
            index -= 1
    
    ## if we have a negative sign requested, take the two's complement form
    if sign == -1:
        posstr = twoc(posstr, len(posstr))
    
    return posstr
