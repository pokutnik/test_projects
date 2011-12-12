# -*- coding: utf-8 -*-
"""
The median of a sequence of numbers X[0], X[1], ..., X[N] is the middle element in terms of their values. More formally, the median of X[0], X[1], ..., X[N] is an element X[I] of the sequence, such that at most half of the elements are larger than X[I] and at most half of the elements are smaller than X[I]. For example, the median of the following sequence:

  X[0] = 7    X[1] = 2    X[2] = 5    X[3] = 2    X[4] = 8    
is 5; the median of the following sequence:

  X[0] = 2    X[1] = 2    X[2] = 5    X[3] = 2       
is 2; and the following sequence:

  X[0] = 1    X[1] = 5    X[2] = 7    
  X[3] = 4    X[4] = 2    X[5] = 8    
has two medians: 4 and 5.

Note that sequences of odd length have only one median, which is equal to X[N/2] after sorting X. In this problem we consider medians of sequences of odd length only.

Write a function:

def double_median(A,B,P,Q,R,S)

that, given:

two non-empty zero-indexed arrays, A (consisting of N integers) and B (consisting of M integers), both sorted in ascending order
two zero-indexed arrays P and Q, each consisting of K indices of array A, such that 0 ≤ P[I] ≤ Q[I] < N for 0 < I < K
two zero-indexed arrays R and S, each consisting of K indices of array B, such that 0 ≤ R[I] ≤ S[I] < M for 0 < I < K
computes medians of K sequences of the form:

  A[P[I], A[P[I]+1], ..., A[Q[I]-1], A[Q[I]], B[R[I]], B[R[I]+1], ..., B[S[I]-1], B[S[I]]
for 0 ≤ I < K, and returns the median of all such medians.

For example, given the following arrays:

  A[0] = -2   A[1] = 4    A[2] = 10   A[3] = 13   
  B[0] = 5    B[1] = 6    B[2] = 8    B[3] = 12    B[4] = 13
  P[0] = 2    P[1] = 1    P[2] = 0
  Q[0] = 3    Q[1] = 2    Q[2] = 3
  R[0] = 0    R[1] = 0    R[2] = 1
  S[0] = 4    S[1] = 0    S[2] = 3
the function should return 8, since:

the median of [10, 13, 5, 6, 8, 12, 13] equals 10,
the median of [4, 10, 5] equals 5,
the median of [−2, 4, 10, 13, 6, 8, 12] equals 8, and
the median of [10, 5, 8] equals 8.
Assume that:

N and M are integers within the range [1..100,000];
K is an integer within the range [1..10,000];
each element of array A is an integer within the range [−1,000,000,000..1,000,000,000];
array A is sorted in non-decreasing order;
each element of array B is an integer within the range [−1,000,000,000..1,000,000,000];
array B is sorted in non-decreasing order;
each element of array P is an integer within the range [0..N−1];
each element of array Q is an integer within the range [0..N−1];
each element of array R is an integer within the range [0..M−1];
each element of array S is an integer within the range [0..M−1];
P[i] ≤ Q[i] and R[i] ≤ S[i] for 0 ≤ i < K;
K is odd and so is Q[i]−P[i]+R[i]−S[i] for 0 ≤ i < K.
Complexity:

expected worst-case time complexity is O(K*(log(N)+log(M)));
expected worst-case space complexity is O(K), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.
"""


def dummy_double_median(A,B,P,Q,R,S):
    assert len(P) == len(Q)
    assert len(R) == len(S)
    assert len(P) == len(R)

    C = []
    for i in xrange(len(P)):
        L = A[P[i]:Q[i]+1]
        M = B[R[i]:S[i]+1]
        T = sorted(L+M)
        #print "T = ", T
        C.append(T[len(T)/2])
    #print "C = ", C
    C.sort()
    r = C[len(C) / 2]
    #print "dm -", r
    return r

from bisect import insort
from array import array

def double_median(A,B,P,Q,R,S):
    A = array("l", A)
    B = array("l", B)
    C = array("l")
    for i in xrange(len(P)):
        a0, a1 = P[i], Q[i]
        b0, b1 = R[i], S[i]

        la = a1 - a0 + 1
        lb = b1 - b0 + 1
        s = min(la, lb) /4 * 2

        #print "Step", step()
        #print A[a0:a1+1], 'ma=', ma()
        #print B[b0:b1+1], 'mb=', mb()

        while s >= 2:
            pa = (a1+a0)/2
            pb = (b1+b0)/2
            ma = A[pa]
            mb = B[pb]

            if ma > mb:
                a1 -= s
                b0 += s
            else:
                a0 += s
                b1 -= s
            la -= s
            lb -= s
            s = min(la, lb) /4 * 2
        if la >= lb:
            L = A[a0:a1+1]
            r = B[b0:b1+1]
        else:
            r = A[a0:a1+1]
            L = B[b0:b1+1]
        for i in r:
            insort(L, i)
        c = L[len(L)/2]
        C.append(c)
    C = sorted(C)
    r = C[len(C) / 2]
    return r


if __name__ == '__main__':
    
    A = [-2, 4, 10, 13]   
    B = [5, 6, 8, 12, 13]
    P = [2, 1 ,0]
    Q = [3, 2 ,3]
    R = [0, 0, 1]
    S = [4, 0, 3]
    #assert dummy_double_median(A, B, P, Q, R, S) == 8

    assert double_median(A, B, P, Q, R, S) == 8

    assert double_median( **{'A': [1, 3, 5, 5], 'B': [2, 4], 'Q': [3, 1, 2], 'P': [1, 0, 0], 'S': [1, 0, 1], 'R': [0, 0, 0]}) == 3 

    from random import randint
    import pickle
    import os    
    import timeit


    def gen(N, K):
        A = []
        B = []
        P = []
        Q = []
        R = []
        S = []

        for i in xrange(N):
            A.append(randint(1, N*10))
            B.append(randint(1, N*10))
        A.sort()
        B.sort()
        for i in xrange(K):
            p = randint(0, N-1)
            q = randint(p, N-1)
            r = randint(1, N-1)
            s = randint(r, N-1)
            if not( (q-p) + (r-s) % 2 ):
                r -= 1
            P.append(p)
            Q.append(q)
            R.append(r)
            S.append(s)
        return A,B,P,Q,R,S

    ## check correct
    A,B,P,Q,R,S = gen(10, 10)
    ddm = dummy_double_median(A, B, P, Q, R, S)
    dm = double_median(A, B, P, Q, R, S)
    assert ddm == dm

    A,B,P,Q,R,S = gen(100, 100)
    ddm = dummy_double_median(A, B, P, Q, R, S)
    dm = double_median(A, B, P, Q, R, S)
    assert ddm == dm
    

    prep = """
from double_median import dummy_double_median, double_median
import pickle
fn = '%s'
with open(fn, 'rb') as f:
    A,B,P,Q,R,S = pickle.load(f)
"""


    ## 5k run

    fn = 'median_5000.dat'
    if os.path.exists(fn):
        with open(fn, 'rb') as f:
            A,B,P,Q,R,S = pickle.load(f)
    else:
        A,B,P,Q,R,S = gen(5000, 3000)
        with open(fn, 'wb') as f:
            pickle.dump((A,B,P,Q,R,S), f)

    t = timeit.Timer("double_median(A, B, P, Q, R, S)", prep % fn)
    print 'step  5k=%f' % t.timeit(1)


    fn = 'median_10000.dat'
    if os.path.exists(fn):
        with open(fn, 'rb') as f:
            A,B,P,Q,R,S = pickle.load(f)
    else:
        A,B,P,Q,R,S = gen(10000, 3000)
        with open(fn, 'wb') as f:
            pickle.dump((A,B,P,Q,R,S), f)
    t = timeit.Timer("double_median(A, B, P, Q, R, S)", prep % fn)
    print 'step  10k=%f' % t.timeit(1)


    fn = 'median_30000.dat'
    if os.path.exists(fn):
        with open(fn, 'rb') as f:
            A,B,P,Q,R,S = pickle.load(f)
    else:
        A,B,P,Q,R,S = gen(30000, 3000)
        with open(fn, 'wb') as f:
            pickle.dump((A,B,P,Q,R,S), f)

    t = timeit.Timer("double_median(A, B, P, Q, R, S)", prep % fn)
    print 'step  30k=%f' % t.timeit(1)
    import cProfile
    cProfile.run("double_median(A, B, P, Q, R, S)")


