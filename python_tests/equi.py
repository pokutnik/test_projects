"""
Task #6
=======

A zero-indexed array A consisting of N integers is given. Anequilibrium
index of this array is any integer P such that 0 ≤ P < N and the sum of
elements of lower indices is equal to the sum of elements of higher
indices, i.e.

A[0] + A[1] + ... + A[P−1] = A[P+1] + ... + A[N−2] + A[N−1].

Sum of zero elements is assumed to be equal to 0. This can happen if P
= 0 or if P = N−1.

For example, consider the following array A consisting of N = 7
elements:

A[0] = -7   A[1] =  1   A[2] = 5
A[3] =  2   A[4] = -4   A[5] = 3
A[6] =  0

P = 3 is an equilibrium index of this array, because A[0] + A[1] + A[2] =
A[4] + A[5] + A[6].

P = 6 is also an equilibrium index, because: A[0] + A[1] + A[2] + A[3]
+ A[4] + A[5] = 0 and there are no elements with indices greater than 6

P = 7 is not an equilibrium index, because it does not fulfill the condition
0 ≤ P < N.

Write a function
    def equi(A)
that, given a zero-indexed array A consisting of N integers, returns any
of its equilibrium indices. The function should return −1 if no equilibrium
index exists.

Assume that:
* N is an integer within the range [0..10,000,000];
* each element of array A is an integer within the range
[−2,147,483,648..2,147,483,647].

For example, given array A such that

A[0] = -7   A[1] =  1   A[2] = 5
A[3] =  2   A[4] = -4   A[5] = 3
A[6] =  0

the function may return 3 or 6, as explained above.
Complexity:
* expected worst-case time complexity is O(N);
* expected worst-case space complexity is O(N), beyond input
storage (not counting the storage required for input arguments).

Elements of input arrays can be modified.
"""


def all_equi(A):
    """ Generator of all equilibrium numbers of A"""
    part_sum = 0
    total = sum(A)
    for i, a in enumerate(A):
        if part_sum * 2 + a == total:
            yield i
        part_sum += a


def equi(A):
    """ Calculate any (actualy first one) equilibrium number
        or retunrn -1
    """
    return all_equi(A).next() or -1


if __name__ == "__main__":
    assert list(all_equi([0])) == [0]
    assert list(all_equi([0, 0])) == [0, 1]
    assert list(all_equi([1, 2, 3, 4, 5])) == []
    assert list(all_equi([-7, 1, 5, 2, -4, 3, 0])) == [3, 6]

    assert equi([0]) == -1
    assert equi([-7, 1, 5, 2, -4, 3, 0]) == 3
