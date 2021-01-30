# 1) Write a function def solution(A) that, given an array A of N integers, returns the smallest positive integer
# (greater than 0) that does not occur in A.
# For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.
# Given A = [1, 2, 3], the function should return 4.
# Given A = [−1, −3], the function should return 1.


def get_min_positive_int(arr):
    """Take care of passing list/tuple of integers since there's no check of input values here.
        Strings are not supported is input value
    """
    max_val = max(arr)
    missing_vals = []
    if max_val <= 0:
        print(f"Smallest positive integer for {arr} is 1")
        return 1
    for x in range(max_val):
        if x not in arr:
            missing_vals.append(x)
    if len(missing_vals) > 0:
        smallest_positive = min(missing_vals)
        print(f"Smallest missing positive integer for {arr} is {smallest_positive}")
    else:
        smallest_positive = max_val + 1
        print(f"Smallest positive integer for {arr} is {smallest_positive}")
    return smallest_positive


print("\nTask 1: Smallest positive integer")
get_min_positive_int([0, 1, 2, 3, 6, 7, 10])
get_min_positive_int([-1, -2, 0])
get_min_positive_int([-1, -2, 0, 1, 2, 3])


# 2)A binary gap within a positive integer N is any maximal sequence of consecutive zeros that is surrounded by ones at
# both ends in the binary representation of N.
# For example, number 9 has binary representation 1001 and contains a binary gap of length 2.
# The number 529 has binary representation 1000010001 and contains two binary gaps: one of length 4 and one of length 3.
# The number 20 has binary representation 10100 and contains one binary gap of length 1.
# The number 15 has binary representation 1111 and has no binary gaps.
# The number 32 has binary representation 100000 and has no binary gaps.
# Write a function:
# def solution(N)
# that, given a positive integer N, returns the length of its longest binary gap.
# The function should return 0 if N doesn't contain a binary gap.
# For example, given N = 1041 the function should return 5, because N has binary representation 10000010001 
# and so its longest binary gap is of length 5.
# Given N = 32 the function should return 0, because N has binary representation '100000' and thus no binary gaps.

def get_binary_gap(number):
    binary = bin(number)[2:]
    bin_gap = len(max(binary.strip('0').strip('1').split('1')))
    if not bin_gap:
        print(f"Number's {number} binary representation {binary} contains no zeros surrounded by ones")
        return 0
    else:
        print(f"Number's {number} binary representation's {binary} max binary gap length is: {bin_gap}")
        return bin_gap


print("\nTask 2: Binary gap")
get_binary_gap(9)
get_binary_gap(529)
get_binary_gap(20)
get_binary_gap(15)
get_binary_gap(32)
get_binary_gap(1041)
get_binary_gap(581)

# 3)An array A consisting of N integers is given. Rotation of the array means that each element is shifted right
# by one index, and the last element of the array is moved to the first place.
# For example, the rotation of array A = [3, 8, 9, 7, 6] is [6, 3, 8, 9, 7]
# (elements are shifted right by one index and 6 is moved to the first place).
# The goal is to rotate array A K times; that is, each element of A will be shifted to the right K times.
# Write a function:
# def solution(A, K)
# that, given an array A consisting of N integers and an integer K, returns the array A rotated K times.
# For example, given
#     A = [3, 8, 9, 7, 6]
#     K = 3
# the function should return [9, 7, 6, 3, 8]. Three rotations were made:
#     [3, 8, 9, 7, 6] -> [6, 3, 8, 9, 7]
#     [6, 3, 8, 9, 7] -> [7, 6, 3, 8, 9]
#     [7, 6, 3, 8, 9] -> [9, 7, 6, 3, 8]
# For another example, given
#     A = [0, 0, 0]
#     K = 1
# the function should return [0, 0, 0]
# Given
#     A = [1, 2, 3, 4]
#     K = 4
# the function should return [1, 2, 3, 4]

print("\nTask 3. Array rotation")


def rotate_array(arr, rotations):
    for x in range(rotations):
        arr_rot = arr[-1:] + arr[:(len(arr) - 1)]
        print(f"Initial array {arr} rotated {rotations} times: {arr_rot}")


rotate_array([3, 8, 9, 7, 6], 3)
