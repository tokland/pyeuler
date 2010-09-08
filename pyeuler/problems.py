#!/usr/bin/python
from toolset import *

def problem1():
    """Add all the natural numbers below 1000 that are multiples of 3 or 5.""" 
    return sum(x for x in xrange(1, 1000) if x % 3 == 0 or x % 5 == 0)

def problem2():
    """Find the sum of all the even-valued terms in the Fibonacci < four million."""
    even_fibonacci = (x for x in fibonacci() if x % 2)
    return sum(takewhile(lambda x: x < 4e6, even_fibonacci))
  
def problem3():
    """Find the largest prime factor of a composite number."""
    return max(prime_factors(600851475143))

def problem4():
    """Find the largest palindrome made from the product of two 3-digit numbers."""
    # A brute-force solution works fine, but we can simplify it a little bit:
    # x * y = "abccda" = 100001a + 10010b + 1100c = 11 * (9091a + 910b + 100c)
    # So at least one of them must be multiple of 11. 
    candidates = (x*y for x in xrange(110, 1000, 11) for y in xrange(x, 1000))
    return max(ifilter(is_palindromic, candidates))

def problem5():
    """What is the smallest positive number that is evenly divisible by all of 
    the numbers from 1 to 20?."""
    return reduce(least_common_multiple, range(2, 20+1))

def problem6():
    """Find the difference between the sum of the squares of the first one 
    hundred natural numbers and the square of the sum."""
    sum_of_squares = sum(x**2 for x in xrange(1, 100+1))
    square_of_sums = sum(xrange(1, 100+1))**2
    return square_of_sums - sum_of_squares

def problem7():
    """What is the 10001st prime number?."""
    return takenth(10001-1, primes())
