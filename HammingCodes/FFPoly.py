import numpy as np

def sanity_pol_check(x, fieldcardinal):
    x = x % fieldcardinal
    last_non_zero = 0
    for i, val in enumerate(x):
        if val != 0:
            last_non_zero = i
    return x[:last_non_zero+1]

class FFPoly:

    def __init__(array, fieldcardinal):
        array = sanity_pol_check(array, fieldcardinal)
        self.fieldcardinal = fieldcardinal
        self.coeffs = array % fieldcardinal

    def __mul__(y):
        assert self.fieldcardinal == y.fieldcardinal
        final_len = len(y.coeffs) + len(self.coeffs)
        res = np.zeros((final_len))
        for i, cox in enumerate(self.coeffs) :
            for j, coy in enumerate(y.coeffs) :
                res[i + j] += cox * coy
        return FFPoly(res, self.fieldcardinal)

    def __add__(y):
        assert self.fieldcardinal == y.fieldcardinal
        rescoeff = np.zeros((max((len(self.coeffs), len(y.coeffs)))))
        rescoeff[:len(self.coeffs):] += self.coeffs
        rescoeff[:len(y.coeffs):] += y.coeffs
        return FFPoly(rescoeff, self.fieldcardinal)

    def __sub__(y):
        assert self.fieldcardinal == y.fieldcardinal
        rescoeff = np.zeros((max((len(self.coeffs), len(y.coeffs)))))
        rescoeff[:len(self.coeffs):] -= self.coeffs
        rescoeff[:len(y.coeffs):] -= y.coeffs
        return FFPoly(rescoeff, self.fieldcardinal)

    def __div__(y):
        assert self.fieldcardinal == y.fieldcardinal
        dividend = sanity_pol_check(self.coeffs, self.fieldcardinal)
        divisor = sanity_pol_check(y.coeffs, y.fieldcardinal)
        if len(divisor) > len(dividend):
            quotient, remainder = FFPoly(np.zeros((1))), self
            return quotient, remainder

        else:
            maincoeffx, maincoeffy = dividend[-1], divisor[-1]
            for k in range(self.fieldcardinal):
                if (maincoeffy * k) % self.fieldcardinal == maincoeffx:
                    quotient = np.zeros((len(dividend) - len(divisor)))
                    quotient[-1] = k
                    substract = np.zeros((len(dividend)))
                    substract[-len(divisor)::] = k * divisor
                    next_div = FFPoly(dividend - substract ,self.fieldcardinal).coeffs
                    next_quot, remainder = FFPoly(next_div, self.fieldcardinal).__div__(divisor)
                    quotient = FFPoly(quotient, self.fieldcardinal).__add__(FFPoly(next_quot, self.fieldcardinal))
                    return quotient.coeffs, remainder

        errmsg = 'this Division failed : ' + str(dividend) + ' | ' + str(divisor)
        raise ValueError(errmsg)
