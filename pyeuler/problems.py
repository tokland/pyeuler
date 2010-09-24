#!/usr/bin/python
import string

import data
from toolset import *

def problem1():
    """Add all the natural numbers below 1000 that are multiples of 3 or 5.""" 
    return sum(x for x in xrange(1, 1000) if x % 3 == 0 or x % 5 == 0)

def problem2():
    """Find the sum of all the even-valued terms in the Fibonacci < 4 million."""
    even_fibonacci = (x for x in fibonacci() if x % 2)
    return sum(takewhile(lambda x: x < 4e6, even_fibonacci))
  
def problem3():
    """Find the largest prime factor of a composite number."""
    return max(prime_factors(600851475143))

def problem4():
    """Find the largest palindrome made from the product of two 3-digit numbers."""
    # A brute-force solution is a bit slow, let's try to simplify it a little bit:
    # x*y = "abccda" = 100001a + 10010b + 1100c = 11 * (9091a + 910b + 100c)
    # So at least one of them must be multiple of 11. 
    candidates = (x*y for x in xrange(110, 1000, 11) for y in xrange(x, 1000))
    return max(c for c in candidates if is_palindromic(c))

def problem5():
    """What is the smallest positive number that is evenly divisible by all of 
    the numbers from 1 to 20?."""
    return reduce(least_common_multiple, range(1, 20+1))

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
    return first(a*b*c for (a, b, c) in triplets if a**2 + b**2 == c**2)
  
def problem10():
    """Find the sum of all the primes below two million."""
    return sum(takewhile(lambda x: x<2e6, primes()))

def problem11():
    """What is the greatest product of four adjacent numbers in any direction 
    (up, down, left, right, or diagonally) in the 20x20 grid?"""
    def grid_get(grid, nr, nc, sr, sc):
        """Return cell for coordinate (nr, nc) is a grid of size (sr, sc).""" 
        return (grid[nr][nc] if 0 <= nr < sr and 0 <= nc < sc else 0)
    grid = [map(int, line.split()) for line in data.problem11.strip().splitlines()]
    # For each cell, get 4 groups in directions E, S, SE and SW
    diffs = [(0, +1), (+1, 0), (+1, +1), (+1, -1)]
    sr, sc = len(grid), len(grid[0])
    return max(product(grid_get(grid, nr+i*dr, nc+i*dc, sr, sc) for i in range(4))
        for nr in range(sr) for nc in range(sc) for (dr, dc) in diffs)
        
def problem12():
    """What is the value of the first triangle number to have over five 
    hundred divisors?"""
    triangle_numbers = (triangle_number(n) for n in count(1))
    return first(tn for tn in triangle_numbers if ilen(divisors(tn)) > 500)

def problem13():
    """Work out the first ten digits of the sum of the following one-hundred 
    50-digit numbers."""
    numbers = (int(x) for x in data.problem13.strip().splitlines())
    return int(str(sum(numbers))[:10])

def problem14():
    """The following iterative sequence is defined for the set of positive 
    integers: n -> n/2 (n is even), n -> 3n + 1 (n is odd). Which starting 
    number, under one million, produces the longest chain?"""
    def collatz_function(n):        
        return ((3*n + 1) if (n % 2) else (n/2))
    @memoize
    def collatz_series_length(n):
        return (1 + collatz_series_length(collatz_function(n)) if n>1 else 0)
    return max(xrange(1, int(1e6)), key=collatz_series_length)

def problem15():
    """How many routes are there through a 20x20 grid?"""
    # To reach the bottom-right corner in a grid of size n we need to move n times
    # down (D) and n times right (R), in any order. So we can just see the 
    # problem as how to put n D's in a 2*n array (a simple permutation),
    # and fill the holes with R's -> permutations(2n, n) = (2n)!/(n!n!) = (2n)!/2n! 
    #   
    # More generically, this is also a permutation of a multiset
    # which has ntotal!/(n1!*n2!*...*nk!) permutations
    # In this problem the multiset is {n.D, n.R}, so (2n)!/(n!n!) = (2n)!/2n!
    n = 20
    return factorial(2*n) / (factorial(n)**2)

def problem16():
    """What is the sum of the digits of the number 2^1000?"""
    return sum(digits_from_num(2**1000))

def problem17():
    """If all the numbers from 1 to 1000 (one thousand) inclusive were written 
    out in words, how many letters would be used?"""
    strings = (get_cardinal_name(n) for n in xrange(1, 1000+1))
    return ilen(c for c in flatten(strings) if c.isalpha())

def problem18():
    """Find the maximum total from top to bottom of the triangle below:"""
    # The note that go with the problem warns that number 67 presents the same
    # challenge but much bigger, where it won't be possible to solve it using 
    # simple brute force. But let's use brute-force here and we'll use the 
    # head later. We test all routes from the top of the triangle. We will find 
    # out, however, that this brute-force solution is much more complicated to 
    # implement (and to understand) than the elegant one.
    def get_numbers(rows):
        """Return groups of "columns" numbers, following all possible ways."""
        for moves in cartesian_product([0, +1], repeat=len(rows)-1):
            indexes = ireduce(operator.add, moves, 0)
            yield (row[index] for (row, index) in izip(rows, indexes))
    rows = [map(int, line.split()) for line in data.problem18.strip().splitlines()]     
    return max(sum(numbers) for numbers in get_numbers(rows))

def problem19():
    """How many Sundays fell on the first of the month during the twentieth 
    century (1 Jan 1901 to 31 Dec 2000)?"""
    def is_leap_year(year):
        return (year%4 == 0 and (year%100 != 0 or year%400 == 0))
    def get_days_for_month(year, month):
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return days[month-1] + (1 if (month == 2 and is_leap_year(year)) else 0)
    years_months = ((year, month) for year in xrange(1901, 2001) for month in xrange(1, 12+1))
    # Skip the last month (otherwise we would be checking for 1 Jan 2001)
    days = (get_days_for_month(y, m) for (y, m) in years_months if (y, m) != (2000, 12))    
    # Let's index Monday with 0 and Sunday with 6. 1 Jan 1901 was a Tuesday (1)
    weekday_of_first_day_of_months = ireduce(lambda wd, d: (wd+d) % 7, days, 1)
    return sum(1 for weekday in weekday_of_first_day_of_months if weekday == 6)

def problem20():
    """Find the sum of the digits in the number 100!"""
    return sum(digits_from_num(factorial(100)))

def problem21():
    """Evaluate the sum of all the amicable numbers under 10000."""
    sums = dict((n, sum(proper_divisors(n))) for n in xrange(1, 10000))
    return sum(a for (a, b) in sums.iteritems() if a != b and sums.get(b, 0) == a)

def problem22():
    """What is the total of all the name scores in the file?"""
    contents = data.openfile("names.txt").read()
    names = sorted(name.strip('"') for name in contents.split(","))
    dictionary = dict((c, n) for (n, c) in enumerate(string.ascii_uppercase, 1))
    return sum(i*sum(dictionary[c] for c in name) for (i, name) in enumerate(names, 1))

def problem23():
    """Find the sum of all the positive integers which cannot be written as 
    the sum of two abundant numbers."""
    abundants = set(x for x in xrange(1, 28123+1) if is_perfect(x) == 1)
    return sum(x for x in xrange(1, 28123+1) if not any((x-a in abundants) for a in abundants))

def problem24():
    """What is the millionth lexicographic permutation of the digits 
    0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?"""
    return num_from_digits(index(int(1e6)-1, permutations(range(10), 10)))

def problem25():
    """What is the first term in the Fibonacci sequence to contain 1000 digits?"""
    # See relation between Fibanacci and the golden-ratio for a non brute-force solution
    return first(idx for (idx, x) in enumerate(fibonacci(), 1) if x >= 10**999)

def problem26():
    """Find the value of d < 1000 for which 1/d contains the longest recurring 
    cycle in its decimal fraction part."""
    def division(numerator, denominator):
        """Return (quotient, (decimals, cycle_length)) for numerator / denomominator."""
        def recursive(numerator, denominator, quotients, remainders):
            q, r = divmod(numerator, denominator)
            if r == 0:
                return (quotients + [q], 0)
            elif r in remainders:
                return (quotients, len(remainders) - remainders.index(r))
            else:       
                return recursive(10*r, denominator, quotients + [q], remainders + [r])
        decimals = recursive(10*(numerator % denominator), denominator, [], [])            
        return (numerator/denominator, decimals)
    # A smarter (and much faster) solution: countdown from 1000 getting cycles' 
    # length, and break when a denominator is lower the the current maximum 
    # length (since a cycle cannot be larger than the denominator itself).
    return max(xrange(2, 1000), key=lambda d: division(1, d)[1][1])

def problem27():
    """Find the product of the coefficients, a and b, for the quadratic 
    expression that produces the maximum number of primes for consecutive
    values of n, starting with n = 0."""
    def function(n, a, b):
        return n**2 + a*n + b
    def primes_for_a_b(a_b):
        return takewhile(is_prime, (function(n, *a_b) for n in count(0)))
    # b must be prime so n=0 yields a prime (b itself)
    b_candidates = list(x for x in xrange(1000) if is_prime(x))
    candidates = ((a, b) for a in xrange(-1000, 1000) for b in b_candidates)    
    return product(max(candidates, key=compose(ilen, primes_for_a_b)))

def problem28():
    """What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral 
    formed in the same way?"""
    return 1 + sum(4*(n - 2)**2 + 10*(n - 1) for n in xrange(3, 1001+1, 2)) 
  
def problem29():
    """How many distinct terms are in the sequence generated by a**b for 
    2 <= a <= 100 and 2 <= b <= 100?"""
    return ilen(unique(a**b for a in xrange(2, 100+1) for b in xrange(2, 100+1)))
  
def problem30():
    """Find the sum of all the numbers that can be written as the sum of fifth 
    powers of their digits."""
    candidates = xrange(2, 6*(9**5))
    return sum(n for n in candidates if sum(x**5 for x in digits_from_num(n)) == n)

def problem31():
    """How many different ways can 2 pounds be made using any number of coins?"""
    def get_weights(units, remaining):
        """Return weights that sum 'remaining'. Pass units in descending order.  
        get_weigths([4,2,1], 5) -> (0,0,5), (0,1,3), (0,2,1), (1,0,1)"""   
        if len(units) == 1 and remaining % units[0] == 0:
            # Make it generic, do not assume that last unit is 1
            yield (remaining/units[0],)
        elif units:
            for weight in xrange(0, remaining + 1, units[0]):
                for other_weights in get_weights(units[1:], remaining - weight):
                   yield (weight/units[0],) + other_weights
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    return ilen(get_weights(sorted(coins, reverse=True), 200))

def problem32():
    """Find the sum of all products whose multiplicand/multiplier/product 
    identity can be written as a 1 through 9 pandigital"""
    def get_permutation(ndigits):
        return ((num_from_digits(ds), list(ds)) for ds in permutations(range(1, 10), ndigits))
    def get_multiplicands(ndigits1, ndigits2):
        return cartesian_product(get_permutation(ndigits1), get_permutation(ndigits2))
    # We have two cases for A * B = C: 'a * bcde = fghi' and 'ab * cde = fghi' 
    # Also, since C has always 4 digits, 1e3 <= A*B < 1e4
    candidates = chain(get_multiplicands(1, 4), get_multiplicands(2, 3))
    return sum(unique(a*b for ((a, adigits), (b, bdigits)) in candidates 
        if a*b < 1e4 and is_pandigital(adigits + bdigits + digits_from_num(a*b))))
        
def problem33():
    """There are exactly four non-trivial examples of this type of fraction, 
    less than one in value, and containing two digits in the numerator and 
    denominator. If the product of these four fractions is given in its lowest 
    common terms, find the value of the denominator."""
    def reduce_fraction(num, denom):
        gcd = greatest_common_divisor(num, denom)
        return (num / gcd, denom / gcd)
    def is_curious(numerator, denominator):
        if numerator == denominator or numerator % 10 == 0 or denominator % 10 == 0:
            return False
        # numerator / denominator = ab / cd
        (a, b), (c, d) = map(digits_from_num, [numerator, denominator])
        reduced = reduce_fraction(numerator, denominator)
        return (b == c and reduce_fraction(a, d) == reduced or 
                a == d and reduce_fraction(b, c) == reduced) 
    curious_fractions = ((num, denom) for num in xrange(10, 100) 
        for denom in xrange(num+1, 100) if is_curious(num, denom))
    numerator, denominator = map(product, zip(*curious_fractions))
    return reduce_fraction(numerator, denominator)[1]

def problem34():
    """Find the sum of all numbers which are equal to the sum of the factorial 
    of their digits."""
    # Cache digits from 0 to 9 to speed it up a little bit
    dfactorials = dict((x, factorial(x)) for x in xrange(10))
    
    # Upper bound: ndigits*9! < 10^ndigits -> upper_bound = ndigits*9!    
    # That makes 7*9! = 2540160. That's quite a number, so it will be slow.
    #
    # A faster alternative: get combinations with repetition of [0!..9!] in 
    # groups of N (1..7), and check the sum value. Note that the upper bound 
    # condition is in this case harder to apply.
    upper_bound = first(n*dfactorials[9] for n in count(1) if n*dfactorials[9] < 10**n)
    return sum(x for x in xrange(3, upper_bound) 
        if x == sum(dfactorials[d] for d in digits_from_num_fast(x)))
        
def problem35():
    """How many circular primes are there below one million?"""
    def is_circular_prime(digits):
        return all(is_prime(num_from_digits(digits[r:] + digits[:r])) 
            for r in xrange(len(digits)))
    # We will use only digits (1, 3, 7, and 9) to generate candidates, so we 
    # consider the four one-digit primes separately.
    circular_primes = (num_from_digits(ds) for n in xrange(2, 6+1) 
        for ds in cartesian_product([1, 3, 7, 9], repeat=n) if is_circular_prime(ds))
    return ilen(chain([2, 3, 5, 7], circular_primes))

def problem36():
    """Find the sum of all numbers, less than one million, which are 
    palindromic in base 10 and base 2."""
    # Trivial constraint: a binary number starts with 1, and to be palindromic it  
    # must also end with 1, so it an odd number (thus halving the numbers to check)
    return sum(x for x in xrange(1, int(1e6), 2) 
        if is_palindromic(x, base=10) and is_palindromic(x, base=2))
        
def problem37():
    """Find the sum of the only eleven primes that are both truncatable from 
    left to right and right to left."""
                yield x
    def truncatable_primes():
        for n in count(2):
            groups = ([[3,7]]+[[1,3,7,9]]*(n-2)+[[3,7]] if n > 2 else [[2,3,5,7]]*n)
            for digits in cartesian_product(*groups):
                x = num_from_digits(digits)                
                if is_prime(x) and all(is_prime(num_from_digits(digits[n:])) and 
                        is_prime(num_from_digits(digits[:-n])) for n in range(1, len(digits))):
                    yield x
    return sum(take(11, truncatable_primes()))
