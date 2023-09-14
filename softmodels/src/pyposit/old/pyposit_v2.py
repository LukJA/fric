# setup_logger.py
import logging
FORMAT = '[%(filename)s:%(lineno)s - %(funcName)12s()][%(levelname)s]  %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
dprint = logging.getLogger('dbg')

class posit_model():
    """ Hardward Posit Model """

    ## posit(es, "0000")
    ## posit (es, (x, n))
    def __init__(self, en: int, p_init):
        self.en = en
        if type(p_init) == str:
            self.p_str = p_init
        elif type(p_init) == tuple:
            self.from_float(p_init[0], p_init[1], en)
        else:
            raise BaseException("Incorrect Init Form")

    def p_set(self, en: int, p_str: str):
        self.en = en
        self.p_str = p_str

    def __repr__(self) -> str:
        return self.p_str

    def sign_str(self) -> str:
        return self.p_str[0]
    
    
    def regime_len(self) -> int:
        if self.p_str[1] == "1":
            return self.p_str[1:].find("0")
        if self.p_str[1] == "0":
            return self.p_str[1:].find("1")
    
    def regime_str(self) -> str:
        return self.p_str[1: 1 + self.regime_len()]

    def rbar_len(self) -> int:
        if self.regime_len() + 1 == len(self.p_str):
            return 0
        else:
            return 1
    
    def rbar_str(self) -> str:
        if self.rbar_len:
            return self.p_str[1 + self.regime_len()]
        else:
            return ""

    def exp_len(self) -> int:
        rem = len(self.p_str) - 1 - self.regime_len() - self.rbar_len()
        if rem < self.en:
            return rem
        else:
            return self.en
        
    def exp_str(self) -> str:
        if self.exp_len():
            return self.p_str[2 + self.regime_len(): 2 + self.regime_len() + self.exp_len()]
        else:
            return ""

    def frac_len(self) -> int:
        return len(self.p_str) - (1 + self.regime_len() + self.rbar_len() + self.exp_len())
    
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
        dprint.debug(f"S: {s} R: {r} E: {e} F: {f}")
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
            self.p_str = twoc(self.p_str, len(self.p_str))

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
        dprint.debug(f"S: {s} R: {r} E: {e} F: {f}")
        return (1 + f) * 2**(e) * sf**(r) * s


    def from_float(self, x: float, n: int, es: int):
        dprint.debug(f"[{x}]")
        if x == float(0.0):
            self.en = es
            self.p_str = "0"*n
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
            posstr = twoc(posstr, len(posstr))
        dprint.debug(f" -> {posstr} {es}")
        self.en = es
        self.p_str = posstr


    def __add__(self, other):
        if self.en != other.en or len(self.p_str) != len(other.p_str):
            raise BaseException("Posit Format Mismatch")

        ## copy format specifiers
        es = self.en
        n = len(self.p_str) 
        sf = 2**(es) # es # shift factor format defined

        dprint.debug(f"A: {self}, B: {other}")

        ## extract signs, take the complement to get the positive form
        a_sign = 1 if self.sign_str() == "0" else -1
        if a_sign == -1:
            self.p_str = twoc(self.p_str, len(self.p_str))
        b_sign = 1 if other.sign_str() == "0" else -1
        if b_sign == -1:
            other.p_str = twoc(other.p_str, len(other.p_str))
        
        ## extract mantissa
        a_mantissa = self.frac_str()
        b_mantissa = other.frac_str()

        ## extract exponent
        a_exponent = self.exp_str()
        b_exponent = other.exp_str()
        ## extend to signed 1b
        if len(a_exponent) < 8: # sign extend
            a_exponent = "0"*(8-len(a_exponent)) + a_exponent
        if len(b_exponent) < 8: # sign extend
            b_exponent = "0"*(8-len(b_exponent)) + b_exponent

        ## extract regime numeric values
        a_rbar = self.rbar_str()
        a_reg_len = self.regime_len()
        b_rbar = other.rbar_str()
        b_reg_len = other.regime_len()

        # decode  values
        a_regime = gen_bin_s(a_reg_len, 8)
        if a_rbar == "1":
            a_regime = twoc(a_regime, 8) # negate
        else:
            a_regime = bin_add_s(a_regime, "11111111") # -1

        b_regime = gen_bin_s(b_reg_len, 8)
        if b_rbar == "1":
            b_regime = twoc(b_regime, 8) # negate
        else:
            b_regime = bin_add_s(b_regime, "11111111") # -1

        dprint.debug(f"A~ S:{a_sign} R:{a_regime} E:{a_exponent} F:{a_mantissa}")
        dprint.debug(f"B~ S:{a_sign} R:{b_regime} E:{b_exponent} F:{b_mantissa}")

        ## Check which is bigger and shift to match
        ## if they are equal it doesn't really matter as shift will be 0

        frac_smol = ""
        frac_big = ""
        e_out = "11111111" # -1  pre-shift the p1 in 2C
        r_out = "00000000" # 0
        big_sign = 0
        smol_sign = 0

        dprint.debug(f"a: {bin_g_s(a_regime, b_regime)}")
        dprint.debug(f"b: {(bin_eq_s(a_regime, b_regime) and bin_g_s(a_exponent, b_exponent))}")
        dprint.debug(f"c: {(bin_eq_s(a_regime, b_regime) and bin_eq_s(a_exponent, b_exponent))}")

        ## a is the larger
        if (bin_g_s(a_regime, b_regime)) or \
           (bin_eq_s(a_regime, b_regime) and bin_g_s(a_exponent, b_exponent)) or \
           (bin_eq_s(a_regime, b_regime) and bin_eq_s(a_exponent, b_exponent) and bin_g_u(a_mantissa, b_mantissa)):
 
            dprint.debug("A is larger")

            # calculate the true values of the intermediary format
            e_out = bin_add_s(a_exponent, e_out)
            r_out = a_regime

            ## shift the smaller numbers fraction so that it matches 
            ## add the extra 1 thats hidden (we will do this for big aswell)
            delta_r = bin_sub_s(a_regime, b_regime)
            delta_e = bin_sub_s(a_exponent, b_exponent)

            exp_adj = sf*i_bin_s(delta_r) + i_bin_s(delta_e)

            frac_smol = "1" + b_mantissa
            frac_smol = "0"*(exp_adj) + frac_smol
            frac_big = "1" + a_mantissa
            # copy the signs over
            big_sign = a_sign
            smol_sign = b_sign

        ## b is the larger or they are equal
        else:
            dprint.debug("B is larger or equal")

            # calculate the true values of the intermediary format
            e_out = bin_add_s(b_exponent, e_out)
            r_out = b_regime

            ## shift the smaller numbers fraction so that it matches 
            ## add the extra 1 thats hidden (we will do this for big aswell)
            delta_r = bin_sub_s(b_regime, a_regime)
            delta_e = bin_sub_s(b_exponent, a_exponent)

            exp_adj = sf*i_bin_s(delta_r) + i_bin_s(delta_e)

            frac_smol = "1" + a_mantissa
            frac_smol = "0"*(exp_adj) + frac_smol
            frac_big = "1" + b_mantissa
            # copy the signs over
            big_sign = b_sign
            smol_sign = a_sign

        # extend big to match depth
        frac_big = frac_big + (len(frac_smol) - len(frac_big))*"0"

        dprint.debug(f"big:   0.{frac_big}")
        dprint.debug(f"small: 0.{frac_smol}")

        dprint.debug(f"rout:  {r_out}")
        dprint.debug(f"eout:  {e_out}")

        ## sign control
        # posneg
        if big_sign == 1 and smol_sign == -1:
            dprint.debug("Smaller negative - invert")
            frac_smol = twoc(frac_smol, len(frac_smol))
            dprint.debug(f"big:   0.{frac_big}")
            dprint.debug(f"small: 0.{frac_smol}")
        # negpos
        if big_sign == -1 and smol_sign == 1:
            dprint.debug("Bigger negative - invert smaller and negate answer")
            frac_smol = twoc(frac_smol, len(frac_smol))
            dprint.debug(f"big:   0.{frac_big}")
            dprint.debug(f"small: 0.{frac_smol}")
        # negneg
        if big_sign == -1 and smol_sign == -1:
            dprint.debug("Both negative - negate answer")

        if (big_sign == 1 and smol_sign == -1) or (big_sign == -1 and smol_sign == 1):
            dprint.debug("Negative detected in sum")
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]
            dprint.debug(f"Sum: {frac_big} + {frac_smol} = {f_sum}")
            
            if len(f_sum) > len(frac_big):
                f_sum = f_sum[1:]
        else:
            ## peform the fractional addition
            ## add and zero extend
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]
            dprint.debug(f"Sum: {frac_big} + {frac_smol} = {f_sum}")

            if len(f_sum) > len(frac_smol):
                ## overflow case
                e_out = bin_add_s(e_out, "00000001")
            elif len(f_sum) <= len(frac_smol):
                f_sum = (max(len(frac_smol), len(frac_big)) - len(f_sum))*"0" + f_sum

        dprint.debug(f"Final Sum: 0.{f_sum}")

        ## normalise the sum (i.e. reshift until the first 1 is gone)
        x = f_sum.find("1")
        if x > -1:
            dprint.debug(f"First 1 at position {x}") 
            f_sum = f_sum[x + 1:]
            dprint.debug(f"C Normalised by {x + 1} to get: 1.{f_sum}")
        else:
            dprint.debug("Fraction is all 0s - answer is 0.0")
            x = 0
            r_out = "10000000" ## force regime exceedence - set to max negative
            #raise Exception("Zero Case")

        ## update the exponent with the normalised shift
        dprint.debug(f"E out moved from {e_out}")
        e_out = bin_add_s(e_out, "00000001") # +1
        e_out = bin_sub_s(e_out, gen_bin_s(x, 8)) # -x
        dprint.debug(f"E out moved to {e_out}")

        ## recompare the regime and the exponent levels
        dprint.debug(f"Prenormal: R:{r_out} E:{e_out} F:(1).{f_sum}")
        # case 1 - exponent too large, greater than 0:
        if bin_geq_s(e_out, gen_bin_s(2**es, 8)):
            dprint.debug("E too big")
            # shift over until its constrained
            # allowed bits equals es - so shift is the position of the first 1 minus es
            shiftamt = (len(e_out) - e_out.find("1")) - es
            dprint.debug(f">> {shiftamt}")
            e_out = bin_sub_s(e_out, gen_bin_s(2**es*shiftamt, 8))
            r_out = bin_add_s(r_out, gen_bin_s(shiftamt, 8))
        # case 2 - exponent too small:
        elif bin_g_s(gen_bin_s(0, 8), e_out):
            dprint.debug("E too small")
            # shift up until its positive
            tc = twoc(e_out, 8)
            shiftamt = (len(tc) - tc.find("1"))
            dprint.debug(f"<< {shiftamt}")
            e_out = bin_add_s(e_out, gen_bin_s(2**es*shiftamt, 8))
            r_out = bin_sub_s(r_out, gen_bin_s(shiftamt, 8))
        dprint.debug(f"Posnormal: R:{r_out} E:{e_out} F:(1).{f_sum}")

        ## we now have all the ideal required parts, convert to closest posit repr by available space
        ## TODO: rounding probably invalid for frac len ~ 0 region
        ## calculate lengths required by each field
        sign_ = 1
        regime_ = - i_bin_s(r_out) if i_bin_s(r_out) < 0 else i_bin_s(r_out) + 1
        rnought_ = 1
        exponent_ = es
        if sign_ + regime_ > n:
            dprint.debug("Infinity")
        elif sign_ + regime_ == n:
            f_sum = ""
            e_out = gen_bin_s(0, 8)
        elif sign_ + regime_ + rnought_ == n:
            #  s r rbar 
            f_sum = ""
            e_out = gen_bin_s(0, 8)
        elif sign_ + regime_ + rnought_ + exponent_ == n:
            #  s r rbar e
            # no frac
            f_sum = ""
        else:
            ## absolute allowed fraction length
            f_depth = n - (sign_ + regime_ + rnought_ + exponent_)
            
            ## remove trailing zeroes 
            f_sum = f_sum[:f_sum.rfind("1")+1]
            ## extend if necessary to required depth
            f_sum = f_sum + "0"*(f_depth- len(f_sum))

            dprint.debug(f"Length : {len(f_sum)} Allowed : {f_depth} -> (1).{f_sum[:f_depth]}({f_sum[f_depth:]})")
            
            if (len(f_sum) == f_depth):
                ## then we are exact
                dprint.debug("Repr Exact")
                pass
            else:
                ## non-exact representation will occur
                ## if the mantissa has a bit that will fall off the edge, use it to round over the final bit?


                ## we need to round
                digit_n = f_sum[f_depth-1]
                digit_n1 = f_sum[f_depth]
                dprint.debug(f"{digit_n}-{digit_n1}-({f_sum[f_depth+1:]})")

                ## round down case
                if digit_n1 == "0":
                    dprint.debug(f"Round Down {f_sum} {f_depth}")
                    #dprint.debug(f"Reasons: {f_sum[f_depth-1]},{f_sum[f_depth]} = '0X' or '10'")
                    f_sum = f_sum[:f_depth]
                ## round up case
                else:
                    dprint.debug("Round Up")
                    #dprint.debug(f"Reasons: {f_sum[f_depth-1]},{f_sum[f_depth]} != '0X' or '10'")
                    ## shift right to get MSB
                    dprint.debug(f"f og: {f_sum}")
                    f_sum = "1" + f_sum
                    dprint.debug(f"f ex: {f_sum}")
                    ## add one at LSB-1 and take the floor
                    roundup = bin(int(f_sum, 2) + int("1"+"0"*( len(f_sum)-f_depth-1), 2))[2:]
                    dprint.debug(f"rup: {roundup}")
                    ## check for overflow
                    if len(roundup) > len(f_sum):
                        raise BaseException("Rounding Overflow Not Implemented")
                    
                    ## shift left one and round up
                    f_sum = roundup[1: f_depth+1]
                    dprint.debug(f"f rd: {f_sum}")


        ## compute the approximate fractional value
        # dprint.debug(f"Poscat: R:{r_out} E:{e_out} F:(1).{f_sum}")
        # f = 2**(-len(f_sum))*int("0" + f_sum, 2)
        # sff = 2**(2**(es))
        # dprint.debug(f"R: {r_out} E: {e_out} F: {f}")
        # dprint.debug(f"Out: {1+f} * { 2**(i_bin_s(e_out))} * {sff**(i_bin_s(r_out))}")
        # dprint.debug(f"Approx: {(1 + f) * 2**(i_bin_s(e_out)) * sff**(i_bin_s(r_out))}")


        finalstr = "0"
        # dprint.debug(f"0 + R{regime_}*X + R_{'Y' if (regime_ + 1 < n) else ''} + E{e_out[-es:]} + F{f_sum}")
            
        if i_bin_s(r_out) < 0:
            finalstr += (regime_)*"0" + "1" 
        else:
            finalstr += (regime_)*"1" + "0" 
        ## chop off the excess to fit the posit repr
        finalstr += "0"*(exponent_- len(e_out[-es:])) + e_out[-es:] + f_sum
        finalstr = finalstr[:n]

        ## if we really want the negative soln, invert it
        if big_sign == -1:
            finalstr = twoc(finalstr, len(finalstr))
            dprint.debug("Taking negation of answer")
        dprint.debug(finalstr)

        ## must return original object signs
        if a_sign == -1:
            self.p_str = twoc(self.p_str, len(self.p_str))
        if b_sign == -1:
            other.p_str = twoc(other.p_str, len(other.p_str))

        return posit_model(es, finalstr)

    def __sub__(self, other):
        ## subtract other from self
        ## complement other and add
        a = self
        b = other
        b.p_str = twoc(b.p_str, len(b.p_str))
        x = a + b
        return x
                

if __name__ == "__main__":

    a = posit_model(2, (12, 32))
    b = posit_model(2, (12, 32))
    c = a + b
    dprint.debug(c.to_float())

