#!/usr/bin/python
from toolset import *
import data

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
    # x*y = "abccda" = 100001a + 10010b + 1100c = 11 * (9091a + 910b + 100c)
    # So at least one of them must be multiple of 11 (let's say it's x) 
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
    return index(10001-1, primes())
  
def problem8():
    """Find the greatest product of five consecutive digits in the 1000-digit number"""
    digits = (int(c) for c in "".join(data.problem8.strip().splitlines()))
    return max(product(nums) for nums in groups(digits, 5, 1))
  
def problem9():
    """There exists exactly one Pythagorean triplet for which a + b + c = 1000.
    Find the product abc."""
    triplets = ((a, b, 1000-a-b) for a in xrange(1, 999) for b in xrange(a+1, 999))
    return first(a*b*c for (a, b, c) in triplets if a**2+b**2==c**2)
  
def problem10():
    """Find the sum of all the primes below two million."""
    return sum(takewhile(lambda x: x<2e6, primes()))

def _problem11_without_zeros():
    """What is the greatest product of four adjacent numbers in any direction 
    (up, down, left, right, or diagonally) in the 2020 grid?"""
    grid = [map(int, line.split()) for line in data.problem11.strip().splitlines()]
    n, k = len(grid), 4
    pivots1 = [(nr, 0) for nr in xrange(0,n-k+1)] + [(0, nc) for nc in xrange(0,n-k+1)]
    diagonals1 = ([grid[nr+i][nc+i] for i in xrange(n-nr-nc)] for (nr, nc) in pivots1)
    pivots2 = [(nr, n-1) for nr in xrange(0,n-k+1)] + [(0, nc) for nc in xrange(k-1,n)]
    diagonals2 = ([grid[nr+i][nc-i] for i in xrange(nc-nr+1)] for (nr, nc) in pivots2)    
    grids = [grid, transpose(grid), diagonals1, diagonals2]
    return max(product(nums) for g in grids for row in g for nums in groups(row, k, 1))

def problem11():
    """What is the greatest product of four adjacent numbers in any direction 
    (up, down, left, right, or diagonally) in the 2020 grid?"""
    def _grid_get(g, nr, nc):
        return (g[nr][nc] if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) else 0)  
    grid = [map(int, line.split()) for line in data.problem11.strip().splitlines()]
    diffs = [(0, 1), (1, 0), (1, 1), (1, -1)]
    return max(product(_grid_get(grid, nr+i*dr, nc+i*dc) for i in range(4)) 
        for nr in range(len(grid)) for nc in range(len(grid[0])) for (dr, dc) in diffs)
