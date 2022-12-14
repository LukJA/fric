from dbg import logger as dprint
class posit():
    """ Posit numerical object """

    ## pure functions
    def twos_complement(self, s: str, n = None) -> str:
        ## take a string of 1 and 0 2's complement
        ## default behaviour on overflow is a wraparound to 0
        if n is None:
            n = len(s)
        q = s.replace("1", "A")
        q = q.replace("0", "1")
        q = q.replace("A", "0")

        ## add 1 and extend
        q = format(int(q, 2) + 1, 'b')
        if len(q) < n: ## the addition has remove leading zeroes
            q = "0"*(n-len(q)) + q
        elif len(q) > n: ## the addition has overflowed - wrap around
            q = "0"*n
        return q

    ## methods
    def __init__(self, en: int, p_str: str):
        self.en = en
        self.p_str = p_str

    def __repr__(self) -> str:
        return self.p_str

    def get_p_str(self) -> str:
        return self.p_str
        
    def p_set(self, en: int, p_str: str):
        self.en = en
        self.p_str = p_str

    def p_set_complement(self):
        self.p_str = self.twos_complement(self.p_str)

    def sign_str(self) -> str:
        return self.p_str[0]

    def sign_i(self) -> int:
        return 1 if self.sign_str() == "0" else -1

    def regime_len(self) -> int:
        for i in range(1, len(self.p_str)):
            if self.p_str[i] != self.p_str[1]:
                return i-1
        return len(self.p_str)-1

    def rbar_len(self) -> int:
        if self.regime_len() + 1 == len(self.p_str):
            return 0
        else:
            return 1

    def exp_len(self) -> int:
        rem = len(self.p_str) - 1 - self.regime_len() - self.rbar_len()
        if rem < self.en:
            return rem
        else:
            return self.en

    def frac_len(self) -> int:
        return len(self.p_str) - (1 + self.regime_len() + self.rbar_len() + self.exp_len())

    def sign_str(self) -> str:
        return self.p_str[0]

    def regime_str(self) -> str:
        return self.p_str[1: 1 + self.regime_len()]

    def rbar_str(self) -> str:
        if self.rbar_len:
            return self.p_str[1 + self.regime_len()]
        else:
            return ""
    
    def exp_str(self) -> str:
        if self.exp_len():
            return self.p_str[2 + self.regime_len(): 2 + self.regime_len() + self.exp_len()]
        else:
            return ""

    def frac_str(self) -> str:
        if self.frac_len():
            return self.p_str[-self.frac_len():]
        else:
            return ""

    def to_float(self) -> float:
        if int(self.p_str[1:]) == 0:
            return 0 if self.sign_str() == "0" else float("NaN")

        s = int(self.sign_str())
        # if s == 1:
        #     # twos complement negate?

        if self.frac_len():
            f = 2**(-self.frac_len())*int(self.frac_str(), 2)
        else:
            f = 0
        if self.exp_len():
            e = int(self.exp_str(), 2)
        else:
            e = 0

        if self.rbar_str() == "1":
            r = -1*self.regime_len()
        else:
            r = self.regime_len() - 1

        ## does not requires two's invertion, although this may be easier in hardware
        ## twos negating then pos decode is simpler
        sf = 2**(2**(self.en))
        return ( ((1-3*s) + f) * 2**((1-2*s)*(e+s)) * sf**((1-2*s)*r) )

    def to_float_2c(self) -> float:
        if int(self.p_str[1:]) == 0:
            return 0.0 if self.sign_str() == "0" else float("NaN")

        # store sign
        s = int(self.sign_str())
        # convert 
        s = 1 if s  == 0 else -1
        # store original pstr
        p_str = self.p_str
        if s == -1:
            # twos complement negate before the decode 
            self.p_str = self.twos_complement(self.p_str)

        # else s == 0

        if self.frac_len():
            f = 2**(-self.frac_len())*int(self.frac_str(), 2)
        else:
            f = 0
        if self.exp_len():
            e = int(self.exp_str(), 2)
        else:
            e = 0

        if self.rbar_str() == "1":
            r = -1*self.regime_len()
        else:
            r = self.regime_len() - 1

        sf = 2**(2**(self.en))

        # revert complement
        self.p_str = p_str
        return (1 + f) * 2**(e) * sf**(r) * s


    def from_float(self, x: float, n: int, es: int):
        dprint.debug(f"FromFloat() [{x}]")
        if x == float(0.0):
            self.p_set(es, "0"*n)
            return 1

        ## grab sign and store
        if x < 0:
            sign = -1
            x = x*-1
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

        dprint.debug(f"{sign} {r} {e} {x}")

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
            posstr = self.twos_complement(posstr)
        dprint.debug(f" -> {posstr} {es}")
        self.p_set(es, posstr)


    def __add__(self, other):

        ## TODO why dont we support different size formats
        if self.en != other.en or len(self.p_str) != len(other.p_str):
            raise BaseException("Posit Format Mismatch")

        ## copy format specifiers
        es = self.en
        n = len(self.p_str)

        print(f"A: {self}, B: {other}")
        print(f"Approx {self.to_float()} + {other.to_float()}")

        ## extract signs
        a_s = self.sign_i()
        b_s = other.sign_i()

        ## if either is negative, take the complement to get the positive form
        if a_s == -1:
            self.p_set_complement()
        if b_s == -1:
            other.p_set_complement()

        ## extract fraction numeric values
        a_f_s = self.frac_str()
        b_f_s = other.frac_str()
        a_f = 0
        b_f = 0
        if self.frac_len():
            a_f = 2**(-self.frac_len())*int(self.frac_str(), 2)
        if other.frac_len():
            b_f = 2**(-other.frac_len())*int(other.frac_str(), 2)

        ## extract exponent numeric values
        a_e = 0
        b_e = 0
        if self.exp_len():
            a_e = int(self.exp_str(), 2)
        if other.exp_len():
            b_e = int(other.exp_str(), 2)

        ## extract regime numeric values
        if self.rbar_str() == "1":
            a_r = -1*self.regime_len()
        else:
            a_r = self.regime_len() - 1
        if other.rbar_str() == "1":
            b_r = -1*other.regime_len()
        else:
            b_r = other.regime_len() - 1

        print(f"A~ S:{a_s} R:{a_r} E:{a_e} F:{a_f}")
        print(f"B~ S:{b_s} R:{b_r} E:{b_e} F:{b_f}")

        ## Check which is bigger and shift to match
        ## if they are equal it doesn't really matter as shift will be 0

        sf = 2**(es) # es
        frac_smol = ""
        frac_big = ""
        e_out = -1 # pre-shift the p1
        r_out = 0
        big_s = 0
        smol_s = 0
        
        # a >= b
        ## a is the larger
        if (a_r > b_r) or \
        (a_r == b_r and a_e > b_e) or \
        (a_r == b_r and a_e == b_e and a_f >= b_f):
            ## a is the larger
            print("A is larger")
            exp_adj = sf*(a_r-b_r) + (a_e-b_e)
            # use its base exponents
            e_out += a_e
            r_out += a_r
            ## shift the smaller numbers fraction so that it matches 
            ## add the extra 1 thats hidden (we will do this for big aswell)
            frac_smol = "1" + b_f_s
            frac_smol = "0"*(exp_adj) + frac_smol
            frac_big = "1" + a_f_s
            # copy the signs over
            big_s = a_s
            smol_s = b_s
        else:
            ## b is the larger
            print("B is larger")
            exp_adj = sf*(b_r-a_r) + (b_e-a_e)
            e_out += b_e
            r_out += b_r
            ## shift the smaller numbers fraction so that it matches 
            ## add the extra 1 thats hidden (we will do this for big aswell)
            frac_smol = "1" + a_f_s
            frac_smol = "0"*(exp_adj) + frac_smol
            frac_big = "1" + b_f_s
            # copy the signs over
            big_s = b_s
            smol_s = a_s

        # extend big to match depth
        frac_big = frac_big + (len(frac_smol) - len(frac_big))*"0"

        print(f"big:   0.{frac_big}")
        print(f"small: 0.{frac_smol}")

        ## sign control
        # posneg
        if big_s == 1 and smol_s == -1:
            print("Smaller negative - invert")
            frac_smol = self.twos_complement(frac_smol, len(frac_smol))
            print(f"big:   0.{frac_big}")
            print(f"small: 0.{frac_smol}")
        # negpos
        if big_s == -1 and smol_s == 1:
            print("Bigger negative - invert smaller and negate answer")
            frac_smol = self.twos_complement(frac_smol, len(frac_smol))
            print(f"big:   0.{frac_big}")
            print(f"small: 0.{frac_smol}")
        # negpos
        if big_s == -1 and smol_s == -1:
            print("Both negative - negate answer")

        if (big_s == 1 and smol_s) == -1 or (big_s == -1 and smol_s == 1):
            print("Negative detected in sum")
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]
            print(f"Sum: {frac_big} + {frac_smol} = {f_sum}")
            
            if len(f_sum) > len(frac_big):
                f_sum = f_sum[1:]
        else:
            ## peform the fractional addition
            ## add and zero extend
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]
            print(f"Sum: {frac_big} + {frac_smol} = {f_sum}")

            if len(f_sum) > len(frac_smol):
                ## overflow case
                #raise BaseException("Fraction Summation Overflow")
                e_out += 1
            elif len(f_sum) <= len(frac_smol):
                f_sum = (max(len(frac_smol), len(frac_big)) - len(f_sum))*"0" + f_sum

        print(f"Final Sum: 0.{f_sum}")

        ## normalise the sum (i.e. reshift until the first 1 is gone)
        x = f_sum.find("1")
        if x > -1:
            print(f"First 1 at position {x}") 
            f_sum = f_sum[x + 1:]
            print(f"C Normalised by {x + 1} to get: 1.{f_sum}")
        else:
            print("Fraction is all 0s - answer is 0.0")
            x = 0
            r_out = -n ## force regime exceedence

        ## update the exponent with the normalised shift
        print(f"E out moved from {e_out}")
        e_out = e_out - x + 1
        print(f"E out moved to {e_out}")
        ## recompare the regime and the exponent levels
        ## 2^e8 vs 2^2^es^r8
        print(f"Prenormal: R:{r_out} E:{e_out} F:(1).{f_sum}")
        while (e_out >= 2**es):
            e_out -= 2**es
            r_out += 1
        while (e_out < 0):
            e_out += 2**es
            r_out -= 1
        print(f"Posnormal: R:{r_out} E:{e_out} F:(1).{f_sum}")

        ## we now have all the ideal required parts, convert to closest posit repr by available space
        ## TODO: rounding probably invalid for frac len ~ 0 region
        ## calculate lengths required by each field
        sign_ = 1
        ## if ????0 = 0, then ???? = ???????.
        ## if ????0 = 1, then ???? = ???? ??? 1
        regime_ = -r_out if r_out < 0 else r_out + 1
        rnought_ = 1
        exponent_ = es
        if sign_ + regime_ > n:
            print("Infinity")
        elif sign_ + regime_ == n:
            f_sum = ""
            e_out = 0
        elif sign_ + regime_ + rnought_ == n:
            #  s r rbar 
            f_sum = ""
            e_out = 0 
        elif sign_ + regime_ + rnought_ + exponent_ == n:
            #  s r rbar e
            # no frac
            f_sum = ""
        else:
            ## we have some frac space - follow the rounding standard

            # Let ???? and ???? be ????-bit posit values such that the open interval (????, ????) contains ???? but no ????-bit posit value.
            # Let ???? be the ????-bit representation of ????.
            # Let ???? be the (???? + 1)-bit posit value associated with the (???? + 1)-bit representation ????1.
            # if ???? < ???? < ???? or (???? = ???? and LSB of ???? is 0) then
            # return ????
            # else
            # return ????

            ## absolute allowed fraction length
            f_depth = n - (sign_ + regime_ + rnought_ + exponent_)
            
            ## remove trailing zeroes 
            f_sum = f_sum[:f_sum.rfind("1")+1]
            ## extend if necessary to required depth
            f_sum = f_sum + "0"*(f_depth- len(f_sum))

            print(f"Length : {len(f_sum)} Allowed : {f_depth} -> (1).{f_sum[:f_depth]}({f_sum[f_depth:]})")
            
            if (len(f_sum) == f_depth):
                ## then we are exact
                print("Repr Exact")
                pass
            else:
                ## we need to round
                digit_n = f_sum[f_depth-1]
                digit_n1 = f_sum[f_depth]
                print(f"{digit_n}-{digit_n1}-({f_sum[f_depth+1:]})")

                ## round down case
                if digit_n1 == "0":
                    print(f"Round Down {f_sum} {f_depth}")
                    #print(f"Reasons: {f_sum[f_depth-1]},{f_sum[f_depth]} = '0X' or '10'")
                    f_sum = f_sum[:f_depth]
                ## round up case
                else:
                    print("Round Up")
                    #print(f"Reasons: {f_sum[f_depth-1]},{f_sum[f_depth]} != '0X' or '10'")
                    ## shift right to get MSB
                    print(f"f og: {f_sum}")
                    f_sum = "1" + f_sum
                    print(f"f ex: {f_sum}")
                    ## add one at LSB-1 and take the floor
                    roundup = bin(int(f_sum, 2) + int("1"+"0"*( len(f_sum)-f_depth-1), 2))[2:]
                    print(f"rup: {roundup}")
                    ## check for overflow
                    if len(roundup) > len(f_sum):
                        raise BaseException("Rounding Overflow Not Implemented")
                    
                    ## shift left one and round up
                    f_sum = roundup[1: f_depth+1]
                    print(f"f rd: {f_sum}")


        ## compute the fractional value
        print(f"Poscat: R:{r_out} E:{e_out} F:(1).{f_sum}")
        f = 2**(-len(f_sum))*int("0" + f_sum, 2)
        sff = 2**(2**(es))
        print(f"Out: {1+f} * { 2**(e_out)} * {sff**(r_out)}")
        print( (1 + f) * 2**(e_out) * sff**(r_out) )

        finalstr = "0"
        print(f"0 + R{regime_}*X + R_{'Y' if (regime_ + 1 < n) else ''} + E{bin(e_out)[2:]} + F{f_sum}")
        if r_out < 0:
            finalstr += (regime_)*"0" + "1" + bin(e_out)[2:] + f_sum
        else:
            finalstr += (regime_)*"1" + "0" + bin(e_out)[2:] + f_sum
        ## chop off the excess to fit the posit repr
        finalstr = finalstr[:n]

        ## if we really want the negative soln, invert it
        if big_s == -1:
            finalstr = self.twos_complement(finalstr)
            dprint.debug("Taking negation of answer")
        print(finalstr)

        ## if either is negative, reset them back to what we had earlier (software)
        if a_s == -1:
            self.p_set_complement()
        if b_s == -1:
            other.p_set_complement()
        return posit(es, finalstr)

    def __sub__(self, other):
        ## subtract other from self
        ## complement other and add
        a = self
        b = other
        b.p_set_complement()
        x = a + b
        return x
                
        

# x = posit(1, "0001001")
# y = posit(1, "0001111")
# ## 0000101???+000101 3/128

# # print(x)
# # print(x.to_float())
# print(y)
# print(3/128)
# y.from_float(3/128, 7, 1)
# print(y)
# print(y.to_float_2c())

if __name__ == "__main__":
    #print(3/16) # 0001110 7 1
    # x = posit(1, "0001110")
    # print(x, x.to_float_2c())
    # x.from_float(x.to_float_2c(), 7, 1)
    # print(x, x.to_float_2c())

    # print(3/128) # 0000101 7 1
    # x = posit(1, "0000101")
    # print(x, x.to_float_2c())
    # x.from_float(x.to_float_2c(), 7, 1)
    # print(x, x.to_float_2c())

    # x = posit(1, "0000000")
    # x.from_float(-128, 7, 1)
    # print(x, x.to_float())

    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(16.0, 7, 1)
    b.from_float(8, 7, 1)
    assert (a-b).to_float() == 8






