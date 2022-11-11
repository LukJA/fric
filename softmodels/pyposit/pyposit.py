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

x = posit(1, "10000")
print(x)
# print(x.sign_str())
# print(x.regime_len(), x.regime_str())
# print(x.rbar_len(), x.rbar_str())
# print(x.exp_len(), x.exp_str())
# print(x.frac_len(), x.frac_str())
print(x.to_float())