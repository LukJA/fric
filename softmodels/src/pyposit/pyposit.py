"""Posits in Python. What more can I say?"""

from dataclasses import dataclass
from pyposit.operations.logic import twoc
from pyposit.operations.generation import gen_bin_s, i_bin_s
from pyposit.operations.comparison import bin_g_s, bin_eq_s, bin_g_u, bin_geq_s
from pyposit.operations.arithmetic import bin_add_s, bin_sub_s
from pyposit.conversion import float_to_posit

@dataclass
class PyPositConfig:
    """Configuration of Posit value: numbers of total and exponent bits."""
    n_bits: int
    es: int  # pylint: disable=C0103

    def __eq__(self, other):
        return self.n_bits == other.n_bits and self.es == other.es


class PyPosit:
    """Python Posit impementation."""

    cfg: PyPositConfig
    value: str

    def __init__(self, cfg: PyPositConfig, bit_str: str):
        self.cfg = cfg
        if len(bit_str) != cfg.n_bits:
            raise ValueError(
                f"Bit string of length {len(bit_str)} does not match "
                f"provided configuration value of {cfg.n_bits}.")
        self.value = bit_str

    @classmethod
    def from_float(cls, cfg: PyPositConfig, val: float):
        """Factory method to create bit string from float."""
        return cls(cfg, float_to_posit(val, n=cfg.n_bits, es=cfg.es))
    
    @property
    def float_approximation(self) -> float:
        """Return the closest float approximation."""
    
        s = int(self.value[0])

        if '1' not in self.value[1:]:
            return 0 if self.is_pos else float('inf')

        f = (pow(2, -self.frac_len) * int(self.frac_str, 2) if self.frac_len
             else 0)

        e = int(self.exp_str, 2) if self.exp_len else 0

        r = -self.regime_len if self.rbar_str == '1' else (self.regime_len - 1)

        ## does not requires two's invertion, although this may be easier
        ## in hardware twos negating then pos decode is simpler
        
        sf = pow( 2, pow( 2, self.es ) )

        return (
            ( (1 - 3*s) + f ) *
            pow( 2, (1 - 2*s) * (e + s) ) *
            pow ( sf, (1 - 2*s) * r )
        )
    
    @property
    def float_approximation_2c(self) -> float:
        """Return a float approximation by a different method."""

        s = self.sign

        if '1' not in self.value[1:]:
            return 0 if self.is_pos else float('inf')
        
        original_value = self.value

        if self.is_neg:  # convert to positive representation
            self.value = self.complement
        
        f = (pow(2, -self.frac_len) * int(self.frac_str, 2) if self.frac_len
             else 0)

        e = int(self.exp_str, 2) if self.exp_len else 0

        r = -self.regime_len if self.rbar_str == '1' else (self.regime_len - 1)

        sf = pow( 2, pow( 2, self.es ) )

        # restore original state
        self.value = original_value

        return s * (1 + f) * pow(2, e) * pow(sf, r)

    def __setattr__(self, name, value):
        if self.__dict__.get("_locked", False):
            if name == "value" and len(value) != self.cfg.n_bits:
                raise ValueError(
                    f"Bit string of length {len(value)} does not match "
                    f"provided configuration value of {self.cfg.n_bits}.")
            if name == "cfg":
                raise AttributeError("Posit configuration cannot be changed")

        self.__dict__[name] = value

    def __repr__(self) -> str:
        return (f"{self.cfg.n_bits}-bit posit with {self.es} "
                f"exponent bits, value: {self.value}")

    def __str__(self) -> str:
        return self.value
    
    def __len__(self):
        return self.cfg.n_bits

    def __eq__(self, other):
        return self.cfg == other.cfg and self.value == other.value
        # FIXME: this doesn't account for any duplicate representations

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")

        ## copy format specifiers
        es = self.es
        n = len(self)
        sf = 2**(es) # es # shift factor format defined

        ## extract signs, take the complement to get the positive form
        a_sign = self.sign
        if a_sign == -1:
            self.value = twoc(self.value, len(self.value))
        b_sign = other.sign
        if b_sign == -1:
            other.value = twoc(other.value, len(other.value))
        
        ## extract mantissa
        a_mantissa = self.frac_str
        b_mantissa = other.frac_str

        ## extract exponent
        a_exponent = self.exp_str
        b_exponent = other.exp_str
        ## extend to signed 1b
        if len(a_exponent) < 8: # sign extend
            a_exponent = "0"*(8-len(a_exponent)) + a_exponent
        if len(b_exponent) < 8: # sign extend
            b_exponent = "0"*(8-len(b_exponent)) + b_exponent

        ## extract regime numeric values
        a_rbar = self.rbar_str
        a_reg_len = self.regime_len
        b_rbar = other.rbar_str
        b_reg_len = other.regime_len

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

        ## Check which is bigger and shift to match
        ## if they are equal it doesn't really matter as shift will be 0

        frac_smol = ""
        frac_big = ""
        e_out = "11111111" # -1  pre-shift the p1 in 2C
        r_out = "00000000" # 0
        big_sign = 0
        smol_sign = 0

        ## a is the larger
        if (bin_g_s(a_regime, b_regime)) or \
           (bin_eq_s(a_regime, b_regime) and bin_g_s(a_exponent, b_exponent)) or \
           (bin_eq_s(a_regime, b_regime) and bin_eq_s(a_exponent, b_exponent) and bin_g_u(a_mantissa, b_mantissa)):

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

        ## sign control
        # posneg
        if big_sign == 1 and smol_sign == -1:
            frac_smol = twoc(frac_smol, len(frac_smol))
        # negpos
        if big_sign == -1 and smol_sign == 1:
            frac_smol = twoc(frac_smol, len(frac_smol))
        # negneg
        if big_sign == -1 and smol_sign == -1:
            pass # both negative, negate answer
        if (big_sign == 1 and smol_sign == -1) or (big_sign == -1 and smol_sign == 1):
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]
            
            if len(f_sum) > len(frac_big):
                f_sum = f_sum[1:]
        else:
            ## peform the fractional addition
            ## add and zero extend
            f_sum = bin(int(frac_big, 2) + int(frac_smol, 2))[2:]

            if len(f_sum) > len(frac_smol):
                ## overflow case
                e_out = bin_add_s(e_out, "00000001")
            elif len(f_sum) <= len(frac_smol):
                f_sum = (max(len(frac_smol), len(frac_big)) - len(f_sum))*"0" + f_sum

        ## normalise the sum (i.e. reshift until the first 1 is gone)
        x = f_sum.find("1")
        if x > -1:
            f_sum = f_sum[x + 1:]
        else:
            x = 0
            r_out = "10000000" ## force regime exceedence - set to max negative
            #raise Exception("Zero Case")

        ## update the exponent with the normalised shift
        e_out = bin_add_s(e_out, "00000001") # +1
        e_out = bin_sub_s(e_out, gen_bin_s(x, 8)) # -x

        ## recompare the regime and the exponent levels
        # case 1 - exponent too large, greater than 0:
        if bin_geq_s(e_out, gen_bin_s(2**es, 8)):
            # shift over until its constrained
            # allowed bits equals es - so shift is the position of the first 1 minus es
            shiftamt = (len(e_out) - e_out.find("1")) - es
            e_out = bin_sub_s(e_out, gen_bin_s(2**es*shiftamt, 8))
            r_out = bin_add_s(r_out, gen_bin_s(shiftamt, 8))
        # case 2 - exponent too small:
        elif bin_g_s(gen_bin_s(0, 8), e_out):
            # shift up until its positive
            tc = twoc(e_out, 8)
            shiftamt = (len(tc) - tc.find("1"))
            e_out = bin_add_s(e_out, gen_bin_s(2**es*shiftamt, 8))
            r_out = bin_sub_s(r_out, gen_bin_s(shiftamt, 8))

        ## we now have all the ideal required parts, convert to closest posit repr by available space
        ## TODO: rounding probably invalid for frac len ~ 0 region
        ## calculate lengths required by each field
        sign_ = 1
        regime_ = - i_bin_s(r_out) if i_bin_s(r_out) < 0 else i_bin_s(r_out) + 1
        rnought_ = 1
        exponent_ = es
        if sign_ + regime_ > n:
            pass # infinity
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
            
            if (len(f_sum) == f_depth):
                ## then we are exact
                pass
            else:
                ## non-exact representation will occur
                ## if the mantissa has a bit that will fall off the edge, use it to round over the final bit?


                ## we need to round
                digit_n = f_sum[f_depth-1]
                digit_n1 = f_sum[f_depth]

                ## round down case
                if digit_n1 == "0":
                    #dprint.debug(f"Reasons: {f_sum[f_depth-1]},{f_sum[f_depth]} = '0X' or '10'")
                    f_sum = f_sum[:f_depth]
                ## round up case
                else:
                    ## shift right to get MSB
                    f_sum = "1" + f_sum

                    ## add one at LSB-1 and take the floor
                    roundup = bin(int(f_sum, 2) + int("1"+"0"*( len(f_sum)-f_depth-1), 2))[2:]

                    ## check for overflow
                    if len(roundup) > len(f_sum):
                        raise BaseException("Rounding Overflow Not Implemented")
                    
                    ## shift left one and round up
                    f_sum = roundup[1: f_depth+1]


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

        ## must return original object signs
        if a_sign == -1:
            self.value = twoc(self.value, len(self.value))
        if b_sign == -1:
            other.value = twoc(other.value, len(other.value))

        return self.__class__(cfg=self.cfg, bit_str=finalstr)

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.cfg != other.cfg:
            raise ValueError("Configuration mismatch!")
        
        # get complement of other as object and use __add__
        other_comp = self.__class__(cfg=self.cfg, bit_str=other.complement)

        return self + other_comp
    
    # TOOD: implement iadd and isub
    
    @property
    def es(self):
        return self.cfg.es

    @property
    def sign(self) -> int:
        """Return sign of value."""
        return 1 if self.value[0] == '0' else -1

    @property
    def is_pos(self):
        return self.sign == 1
    
    @property
    def is_neg(self):
        return self.sign == -1
    
    @property
    def complement(self) -> str:
        """Get 2's complement of value as a string."""
        return twoc(self.value, self.cfg.n_bits)
    
    @property
    def regime_len(self):
        return self.value[1:].find( '0' if self.value[1] == '1' else '1' )
    
    @property
    def rbar_len(self):
        return 0 if self.regime_len + 1 == len(self) else 1
    
    @property
    def exp_len(self):
        rem = len(self) - 1 - self.regime_len - self.rbar_len
        return rem if rem < self.es else self.es
    
    @property
    def frac_len(self):
        return len(self) - 1 - self.regime_len - self.rbar_len - self.exp_len
    
    @property
    def regime_str(self):
        return self.value[ 1 : (self.regime_len + 1) ]
    
    @property
    def rbar_str(self):
        return self.value[1 + self.regime_len] if self.rbar_len else ''
    
    @property
    def exp_str(self):
        start_idx = 2 + self.regime_len
        return self.value[ start_idx : (start_idx + self.exp_len) ]
    
    @property
    def frac_str(self):
        frac_len = self.frac_len
        return self.value[-frac_len:] if frac_len else ''
