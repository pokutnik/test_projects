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

def number_of_zeros(S):
    L = len(S)
    
    zeros = 1  # zeros count
    s = 0  # zeros in column  
    num = 0  # current number
    
    p10_, p10 = (0, 1)  # 10^(l-1) and 10^l  divided by modulo

    for l in xrange(L - 1):
        k = int(S[-l - 1])  # current digit
        lp = l * p10_
        if k == 0:
            zeros += num + 9 * lp + 1
        else:
            zeros += p10 + (k+9) * lp 
        num += k * p10
        p10_, p10 = (p10, (p10 * 10) % modulo)

    l = L - 1
    zeros += (int(S[0]) - 1) * l * p10_
    return zeros % modulo


def direct(S):
    """ dummy algorithm. was used for testing """
    N = int(S)
    zeros = lambda i: sum(1 if c == '0' else 0 for c in str(i))
    return sum(zeros(i) for i in xrange(N + 1))


if __name__ == "__main__":
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

    t = timeit.Timer("""
      number_of_zeros(S)
    """, "from zeros import number_of_zeros; S = '1234567890'*1000")
    print 'time to calculate with L=10000 %f seconds' % t.timeit(100)
    # ~ 0.03 seconds on i3 processor laptop
