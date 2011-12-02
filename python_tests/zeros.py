"""
Task #2
=======

A positive integer N is given. Consider the sequence of numbers
[0, 1, ..., N]. What is the total number of zeros in the decimal
representations of these numbers?

N can be very large. Hence, it is given in the form of a non-empty string
S of length L, containing a decimal representation of N. S contains no
leading zeros.

Write a function:
    def number_of_zeros(S)
that, given a string S, which is a decimal representation of some positive
integer N, returns the total number of zeros in the decimal
representations of numbers [0, 1, ..., N]. If the result exceeds
1,410,000,016, the function should return the remainder from the
division of the result by 1,410,000,017.

For example, for S="100" the function should return 12 and for S="219"
it should return 42.

Assume that:
* L is an integer within the range [1..10,000];
* string S consists only of digits (0-9);
* string S contains no leading zeros.

Complexity:
* expected worst-case time complexity is O(L);
* expected worst-case space complexity is O(L) (not counting the
storage required for input arguments).

"""

modulo = 1410000017
# here we need remainder as result
# so we'll tuncate all big numbers by modulo

ten_power = [1]


def warmup(n):
    """
    Prepare cache table of 10 ** i by modulo
    to not multiply big numbers
    """

    if(n > len(ten_power)):
        d = ten_power[-1]
        for i in xrange(len(ten_power), n):
            d *= 10
            d %= modulo
            ten_power.append(d)


def Z9(l):
    """
        Calculate zeros from 0 to l nines, without counting leading zeros
        Z9(2) = number_of_zeros("99")
        Z9(3) = number_of_zeros("999")

            1 2 . . . l
            -----------
            9 9 . . . 9     \
                      .     |
                      .     += z9
                      .     |
                      0     /

    """
    z9 = sum(9 * i * ten_power[i - 1] for i in xrange(1, l)) + 1
    return z9


def zeros_part(k, l):
    """ zeros (without leading) from "k-1 9 9 9 9 9 9" (l nines) to 0
        k-1 9 9 9 9 9 9     \
         .                  |
         .                  += s
         .                  |
         1  0 0 0 0 0 0     /
            9 9 9 9 9 9     \
                      .     |
                      .     += z9
                      .     |
                      0     /
    """
    assert k > 0
    s = (k - 1) * l * ten_power[l - 1] if l else 0
    z9 = Z9(l)
    return z9 + s


def zeros_leading(S):
    """ Calculate zeros including leading zeros

        0 0 ... x y z
             .
             .
             .
        0 0 ... 0 0 1
        0 0 ... 0 0 0
    """
    L = len(S)
    zl = 0  # zeros count
    s = 0  # zeros in column  
    num = 0  # current number
    revS = S[::-1]  # reversed string
    
    for l, K in enumerate(revS):
        k = int(K)  # current digit
        i = L - l
        if k == 0:
            s = num + 1
        else:
            s = k * l * ten_power[l - 1] + ten_power[l] if l else 1
        zl = zl + s
        num += k * ten_power[l]
    return zl


def number_of_zeros(S):
    l = len(S) - 1
    warmup(l)
    part = zeros_part(int(S[0]), l)
    leading = zeros_leading(S[1:])
    total = part + leading
    return total % modulo


def direct(S):
    """ dummy algorithm. was used for testing """
    N = int(S)
    zeros = lambda i: sum(1 if c == '0' else 0 for c in str(i))
    return sum(zeros(i) for i in xrange(N + 1))


if __name__ == "__main__":
    warmup(10000)
    assert Z9(0) == 1
    assert Z9(1) == 1
    assert Z9(2) == 10
    assert Z9(3) == 190
    assert Z9(4) == 2890

    assert zeros_leading("0") == 1
    assert zeros_leading("1") == 1
    assert zeros_leading("2") == 1
    assert zeros_leading("9") == 1
    assert zeros_leading("00") == 2
    assert zeros_leading("01") == 3
    assert zeros_leading("02") == 4
    assert zeros_leading("03") == 5
    assert zeros_leading("04") == 6
    assert zeros_leading("10") == 12
    assert zeros_leading("11") == 12
    assert zeros_leading("12") == 12
    assert zeros_leading("13") == 12
    assert zeros_leading("20") == 13
    assert zeros_leading("21") == 13
    assert zeros_leading("22") == 13
    assert zeros_leading("99") == 20

    #assert False
    assert number_of_zeros("1") == 1
    assert number_of_zeros("2") == 1
    assert number_of_zeros("3") == 1
    assert number_of_zeros("10") == 2
    assert number_of_zeros("11") == 2
    assert number_of_zeros("12") == 2
    assert number_of_zeros("20") == 3
    assert number_of_zeros("21") == 3
    assert number_of_zeros("22") == 3
    assert number_of_zeros("90") == 10
    assert number_of_zeros("100") == 12
    assert number_of_zeros("101") == 13
    assert number_of_zeros("103") == 15
    assert number_of_zeros("104") == 16
    assert number_of_zeros("105") == 17
    assert number_of_zeros("106") == 18
    assert number_of_zeros("107") == 19
    assert number_of_zeros("108") == 20
    assert number_of_zeros("109") == 21
    assert number_of_zeros("110") == 22
    assert number_of_zeros("200") == 32
    assert number_of_zeros("201") == 33
    assert number_of_zeros("219") == 42
    assert number_of_zeros("9") == 1
    assert number_of_zeros("99") == 10
    assert number_of_zeros("999") == 190
    assert number_of_zeros("9999") == 2890
    assert number_of_zeros("54321") == 21263
    assert number_of_zeros("54331") == 21264
    assert number_of_zeros("50321225546506999999"
            "99999989898787987987987989898985") == 1010678350

    print "Tests PASSED"

    import timeit
    t = timeit.Timer("""
      number_of_zeros(S)
    """, "from zeros import number_of_zeros; S = '1234567890'*1000")
    print 'time to calculate with L=10000 %f seconds' % t.timeit(1)
    # ~ 0.03 seconds on i3 processor laptop

    t = timeit.Timer("""
      number_of_zeros(S)
    """, "from zeros import number_of_zeros; S = '1234567890'*100000")
    print 'time to calculate with L=1000000 %f seconds' % t.timeit(1)
    # ~ 3.5 seconds