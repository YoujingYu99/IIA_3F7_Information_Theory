from math import floor, ceil
from sys import stdout as so
from bisect import bisect


def encode(x, p):

    precision = 32
    one = int(2 ** precision - 1)
    quarter = int(ceil(one / 4))
    half = 2 * quarter
    threequarters = 3 * quarter

    p = dict([(a, p[a]) for a in p if p[a] > 0])

    f = [0]
    for a in p:
        f.append(float(p[a] + f[-1]))
    f.pop()

    f = dict([(a, mf) for a, mf in zip(p, f)])

    y = []
    lo, hi = 0, one
    straddle = 0

    for k in range(len(x)):

        if k % 100 == 0:
            so.write("Arithmetic encoded %d%%    \r" % int(floor(k / len(x) * 100)))
            so.flush()

        lohi_range = hi - lo + 1

        lo = lo + int(ceil(p[x[k]] * lohi_range))
        hi = lo + int(floor(p[x[k]] * lohi_range))

        if lo == hi:
            raise NameError("Zero interval!")

        while True:
            if hi < half:
                y.append(0)
                y.extend(straddle * [1])
                straddle = 0
            elif lo >= half:
                y.append(1)
                y.extend(straddle * [0])
                straddle = 0
                lo = lo - half
                hi = hi - half
            elif lo >= quarter and hi < threequarters:
                straddle = straddle + 1
                lo = lo - quarter
                hi = hi - quarter
            else:
                break
            lo = lo * 2
            hi = hi * 2 + 1

    straddle += 1
    if lo < quarter:
        y.append(0)
        y.extend([1] * straddle)
    else:
        y.append(1)
        y.extend([0] * straddle)

    return y


def decode(y, p, n):
    precision = 32
    one = int(2 ** precision - 1)
    quarter = int(ceil(one / 4))
    half = 2 * quarter
    threequarters = 3 * quarter

    p = dict([(a, p[a]) for a in p if p[a] > 0])

    alphabet = list(p)
    f = [0]
    for a in p:
        f.append(f[-1] + p[a])
    f.pop()

    p = list(p.values())

    y.extend(precision * [0])  # dummy zeros to prevent index out of bound errors
    x = n * [0]  # initialise all zeros

    # initialise by taking first 'precision' bits from y and converting to a number
    value = int("".join(str(a) for a in y[0:precision]), 2)
    y_position = precision  # position where currently reading y
    lo, hi = 0, one

    x_position = 0
    while 1:
        if x_position % 100 == 0:
            so.write("Arithmetic decoded %d%%    \r" % int(floor(x_position / n * 100)))
            so.flush()

        lohi_range = hi - lo + 1
        a = bisect(f, (value - lo) / lohi_range) - 1
        x[x_position] = alphabet[a]

        lo = lo + int(ceil(f[a] * lohi_range))
        hi = lo + int(floor(p[a] * lohi_range))
        if lo == hi:
            raise NameError("Zero interval!")

        while True:
            if hi < half:
                # do nothing
                pass
            elif lo >= half:
                lo = lo - half
                hi = hi - half
                value = value - half
            elif lo >= quarter and hi < threequarters:
                lo = lo - quarter
                hi = hi - quarter
                value = value - quarter
            else:
                break
            lo = 2 * lo
            hi = 2 * hi + 1
            value = 2 * value + y[y_position]
            y_position += 1
            if y_position == len(y):
                break

        x_position += 1
        if x_position == n or y_position == len(y):
            break

    return x
