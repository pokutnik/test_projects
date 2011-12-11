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
#modulo = 141000001700000000000000000000000
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

def number_of_zeros(S):
    L = len(S)
    warmup(L)
    
    zl = 0  # zeros count
    s = 0  # zeros in column  
    num = 0  # current number
    
    for l in xrange(L - 1):
        k = int(S[-l - 1])  # current digit
        if k == 0:
            s = num + 1
        else:
            s = k * l * ten_power[l - 1] + ten_power[l] if l else 1
        num += k * ten_power[l]

        zl += s
        zl += 9 * l * ten_power[l - 1] if l else 0

    k = int(S[0])
    l = L - 1
    s = (k - 1) * l * ten_power[l - 1] if l else 0
    part = s + 1
    total = part + zl
    return total % modulo


def direct(S):
    """ dummy algorithm. was used for testing """
    N = int(S)
    zeros = lambda i: sum(1 if c == '0' else 0 for c in str(i))
    return sum(zeros(i) for i in xrange(N + 1))


if __name__ == "__main__":
    warmup(10000)

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

    assert number_of_zeros('1643407768') == modulo - 1 
    assert number_of_zeros('1643407769') == 0
    assert number_of_zeros('1643407770') == 2

    bigS = "1903212065"
    n_zeros = 1615116639
    n_zeros_mod = n_zeros % modulo
    assert number_of_zeros(bigS) == n_zeros_mod

    bigS = "1410000017000000000000000000000"
    n_zeros = 4186889021588888888888888888916L
    n_zeros_mod = n_zeros % modulo
    assert number_of_zeros(bigS) == n_zeros_mod

    bigS = "1410000017000000000000000000001"
    n_zeros = 4186889021588888888888888888916L + 25 
    n_zeros_mod = n_zeros % modulo
    assert number_of_zeros(bigS) == n_zeros_mod


    print "Tests PASSED"

