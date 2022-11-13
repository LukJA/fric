class posit(object):
    def __init__(self, en: int, p_str: str):
        self.en = en
        self.p_str = p_str

    def __repr__(self) -> str:
        return self.p_str

    def p_set(self, en: int, p_str: str):
        self.en = en
        self.p_str = p_str

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
            self.p_str = self.p_str.replace("1", "A")
            self.p_str = self.p_str.replace("0", "1")
            self.p_str = self.p_str.replace("A", "0")

            ## add 1 and extend
            self.p_str = format(int(self.p_str, 2) + 1, 'b')
            if len(self.p_str) < len(p_str):
                self.p_str = "0"*(len(p_str)- len(self.p_str)) + self.p_str

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
        if x == float(0):
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

        ## sign and regime
        posstr = "0" if sign == 1 else "1"
        posstr += r*"1"+"0" if r > 0 else -1*r*"0"+"1"

        ## exponent - bin string
        e = format(e, 'b')
        if len(e) < es:
            e = "0"*(es - len(e)) + e
        #print(e)
        posstr += e

        if len(posstr) >= n:
            self.p_set(es, posstr[:n])
            return 1

        ## append fraction
        posstr += "0"*(n - len(posstr))
        self.p_set(es, posstr)


        



x = posit(1, "1001001")
## 0000101→+000101 3/128
print(x)
print(x.to_float())
print(x.to_float_2c())
print(x.to_float())

