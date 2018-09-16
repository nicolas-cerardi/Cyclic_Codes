from __future__ import division
import numpy as np


def pol_to_string(polynom, fieldcardinal):
    polstr = str(polynom)
    res = ""
    ints_avail = [str(i) for i in range(fieldcardinal)]
    for char in polstr:
        if char in ints_avail:
            res += char
    return res

def string_to_pol(polynom, q):
    rescoeffs = np.zeros((len(polynom)))
    i = 0
    for char in polynom:
        rescoeffs[i] = int(char)
        i += 1
    return FFPoly(rescoeffs, q)

def sanity_pol_check(x, fieldcardinal):
    x = x % fieldcardinal
    last_non_zero = 0
    for i, val in enumerate(x):
        if val != 0:
            last_non_zero = i
    return x[:last_non_zero+1]



class FFPoly:

    def __init__(self, array, fieldcardinal):
        array = sanity_pol_check(array, fieldcardinal)
        self.fieldcardinal = fieldcardinal
        self.coeffs = array % fieldcardinal

    def __str__(self):
        msg = "( "
        for val in self.coeffs:
            msg = msg + str(int(val)) + " "
        return msg + ")"

    def __mul__(self, y):
        assert self.fieldcardinal == y.fieldcardinal
        final_len = len(y.coeffs) + len(self.coeffs)
        res = np.zeros((final_len))
        for i, cox in enumerate(self.coeffs) :
            for j, coy in enumerate(y.coeffs) :
                res[i + j] += cox * coy
        return FFPoly(res, self.fieldcardinal)

    def __add__(self, y):
        assert self.fieldcardinal == y.fieldcardinal
        rescoeff = np.zeros((max((len(self.coeffs), len(y.coeffs)))))
        rescoeff[:len(self.coeffs):] += self.coeffs
        rescoeff[:len(y.coeffs):] += y.coeffs
        return FFPoly(rescoeff, self.fieldcardinal)

    def __sub__(self, y):
        assert self.fieldcardinal == y.fieldcardinal
        rescoeff = np.zeros((max((len(self.coeffs), len(y.coeffs)))))
        rescoeff[:len(self.coeffs):] -= self.coeffs
        rescoeff[:len(y.coeffs):] -= y.coeffs
        return FFPoly(rescoeff, self.fieldcardinal)

    def __truediv__(self, y):
        assert self.fieldcardinal == y.fieldcardinal
        dividend = sanity_pol_check(self.coeffs, self.fieldcardinal)
        divisor = sanity_pol_check(y.coeffs, y.fieldcardinal)
        if len(divisor) > len(dividend):
            quotient, remainder = FFPoly(np.zeros((1)), self.fieldcardinal), self
            return quotient, remainder

        else:
            maincoeffx, maincoeffy = dividend[-1], divisor[-1]
            for k in range(self.fieldcardinal):
                if (maincoeffy * k) % self.fieldcardinal == maincoeffx:
                    quotient = np.zeros((len(dividend) - len(divisor) + 1))
                    quotient[-1] = k
                    substract = np.zeros((len(dividend)))
                    substract[-len(divisor)::] = k * divisor
                    next_div = FFPoly(dividend - substract ,self.fieldcardinal).coeffs
                    next_quot, remainder = FFPoly(next_div, self.fieldcardinal).__truediv__(FFPoly(divisor, self.fieldcardinal))
                    quotient = FFPoly(quotient, self.fieldcardinal).__add__(FFPoly(next_quot.coeffs, self.fieldcardinal))
                    return quotient, remainder

        errmsg = 'this Division failed : ' + str(dividend) + ' | ' + str(divisor)
        raise ValueError(errmsg)

    def __eq__(self, y):
        assert self.fieldcardinal == y.fieldcardinal
        self.coeffs, y.coeffs = sanity_pol_check(self.coeffs, self.fieldcardinal), sanity_pol_check(y.coeffs, y.fieldcardinal)
        if len(self.coeffs) != len(y.coeffs):
            return False
        for i in range(len(self.coeffs)):
            if self.coeffs[i] != y.coeffs[i]:
                return False
        return True


def MODULATOR(N, Q):
    modulator = np.zeros((N + 1))
    modulator[N] = 1
    modulator[0] = 1
    return FFPoly(modulator, Q)


# to test the class
if __name__=='__main__' :
    a = np.array([1,3,0,0,0,1,1])
    b = np.array([1,0,1,0,1])
    c = np.array([0,0,1,0,0])
    ap, bp, cp = FFPoly(a, 2), FFPoly(b,2), FFPoly(c,2)
    print((ap + bp).coeffs)
    print((bp - ap).coeffs)
    print((ap * cp).coeffs)
    quot, rem = (ap / cp)
    print("Quot : ", quot.coeffs)
    print("Rem : ", rem.coeffs)
