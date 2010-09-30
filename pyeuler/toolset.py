#!/usr/bin/python
import operator
from itertools import ifilter, islice, repeat, groupby
from itertools import count, imap, takewhile, tee, izip
from itertools import chain, starmap, cycle, dropwhile
from itertools import combinations, permutations, product as cartesian_product
from math import sqrt, log, log10, ceil

def take(n, iterable):
    """Take first n elements from iterable"""
    return islice(iterable, n)

def index(n, iterable):
    "Returns the nth item"
    return islice(iterable, n, n+1).next()

def first(iterable):
    """Take first element in the iterable"""
    return iterable.next()

def last(iterable):
    """Take last element in the iterable"""
    return reduce(lambda x, y: y, iterable)

def take_every(n, iterable):
    """Take an element from iterator every n elements"""
    return islice(iterable, 0, None, n)

def drop(n, iterable):
    """Drop n elements from iterable and return the rest"""
    return islice(iterable, n, None)

def ilen(it):
    """Return length exhausing an iterator"""
    return sum(1 for _ in it)

def product(nums):
    """Product of nums"""
    return reduce(operator.mul, nums, 1)

def irange(start_or_end, optional_end=None):
    """Return iterable that counts from start to end (both included)."""
    if optional_end is None:
        start, end = 0, start_or_end
    else:
        start, end = start_or_end, optional_end
    return take(max(end - start + 1, 0), count(start))

def flatten(lstlsts):
    """Flatten a list of lists"""
    return (b for a in lstlsts for b in a)

def compact(it):
    """Filter None values from iterator"""
    return ifilter(bool, it)

def groups(iterable, n, step):
    """Make groups of 'n' elements from the iterable advancing
    'step' elements on each iteration"""
    itlist = tee(iterable, n)
    onestepit = izip(*(starmap(drop, enumerate(itlist))))
    return take_every(step, onestepit)

def compose(f, g):
    """Compose two functions -> compose(f, g)(x) -> f(g(x))"""
    def _wrapper(*args, **kwargs):
        return f(g(*args, **kwargs))
    return _wrapper
  
def iterate(func, arg):
    """After Haskell's iterate: apply function repeatedly."""
    # not functional
    while 1:
        yield arg
        arg = func(arg)                

def accsum(it):
    """Yield accumulated sums of iterable: accsum(count(1)) -> 1,3,6,10,..."""
    return drop(1, ireduce(operator.add, it, 0))

def tails(seq):
    """Get tails of a sequence: tails([1,2,3]) -> [1,2,3], [2,3], [3], []."""
    for idx in xrange(len(seq)+1):
        yield seq[idx:]
     
def ireduce(func, iterable, init=None):
    """Like reduce() but using iterators (a.k.a scanl)"""
    # not functional
    if init is None:
        iterable = iter(iterable)
        curr = iterable.next()
    else:
        curr = init
        yield init
    for x in iterable:
        curr = func(curr, x)
        yield curr

def unique(it):
    """Return items from iterator (order preserved)"""
    # not functional, but fast
    seen = set()
    for x in it:
        if x not in seen:
            seen.add(x)
            yield x

def unique_functional(it):
    """Return items from iterator (order preserved)"""
    # functional but slow as hell. Just a proof-of-concept.
    steps = ireduce(lambda (last, seen), x: ((last, seen) if x in seen 
      else ([x], seen.union([x]))), it, ([], set()))
    return (m for (m, g) in groupby(flatten(last for (last, seen) in steps)))
        
def identity(x):
    """Do nothing and return the variable untouched"""
    return x

def occurrences(it, exchange=False):
    """Return dictionary with occurrences from iterable"""
    return reduce(lambda occur, x: dict(occur, **{x: occur.get(x, 0) + 1}), it, {})

def ncombinations(n, k):
    """Combinations of k elements from a group of n"""
    return cartesian_product(xrange(n-k+1, n+1)) / factorial(k)

def combinations_with_replacement(iterable, r):
    """combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"""
    pool = tuple(iterable)
    n = len(pool)
    for indices in cartesian_product(range(n), repeat=r):
        if sorted(indices) == list(indices):
            yield tuple(pool[i] for i in indices)

# Common maths functions

def fibonacci():
    """Generate fibonnacci serie"""
    get_next = lambda (a, b), _: (b, a+b)
    return (b for (a, b) in ireduce(get_next, count(), (0, 1)))

def factorial(num):
    """Return factorial value of num (num!)"""
    return product(xrange(2, num+1))

def is_integer(x, epsilon=1e-6):
    """Return True if the float x "seems" an integer"""
    return (abs(round(x) - x) < epsilon)

def divisors(n):
    """Return all divisors of n: divisors(12) -> 1,2,3,6,12"""
    all_factors = [[f**p for p in range(fp+1)] for (f, fp) in factorize(n)]
    return (product(ns) for ns in cartesian_product(*all_factors))

def proper_divisors(n):
    """Return all divisors of n except n itself."""
    return (divisor for divisor in divisors(n) if divisor != n)

def is_prime(n):
    """Return True if n is a prime number (1 is not considered prime)."""
    if n < 3:
        return (n == 2)
    elif n % 2 == 0:
        return False
    elif any(((n % x) == 0) for x in xrange(3, int(sqrt(n))+1, 2)):
        return False
    return True

def get_primes(start=2, memoized=False):
    """Yield prime numbers from 'start'"""
    is_prime_fun = (memoize(is_prime) if memoized else is_prime)
    return ifilter(is_prime_fun, count(start))

def digits_from_num_fast(num):
    """Get digits from num in base 10 (fast implementation)"""
    return map(int, str(num))

def digits_from_num(num, base=10):
    """Get digits from num in base 'base'"""
    def recursive(num, base, current):
        if num < base:
            return current+[num]
        return recursive(num/base, base, current + [num%base])
    return list(reversed(recursive(num, base, [])))

def num_from_digits(digits, base=10):
    """Get digits from num in base 'base'"""
    return sum(x*(base**n) for (n, x) in enumerate(reversed(list(digits))) if x)

def is_palindromic(num, base=10):
    """Check if 'num' in base 'base' is a palindrome, that's it, if it can be
    read equally from left to right and right to left."""
    digitslst = digits_from_num(num, base)
    return digitslst == list(reversed(digitslst))

def prime_factors(num, start=2):
    """Return all prime factors (ordered) of num in a list"""
    candidates = xrange(start, int(sqrt(num)) + 1)
    factor = next((x for x in candidates if (num % x == 0)), None)
    return ([factor] + prime_factors(num / factor, factor) if factor else [num])

def factorize(num):
    """Factorize a number returning occurrences of its prime factors"""
    return ((factor, ilen(fs)) for (factor, fs) in groupby(prime_factors(num)))

def greatest_common_divisor(a, b):
    """Return greatest common divisor of a and b"""
    return (greatest_common_divisor(b, a % b) if b else a)

def least_common_multiple(a, b): 
    """Return least common multiples of a and b"""
    return (a * b) / greatest_common_divisor(a, b)

def triangle(x):
    """The nth triangle number is defined as the sum of [1,n] values."""
    return (x*(x+1))/2

def is_triangle(x):
    return is_integer((-1 + sqrt(1 + 8*x)) / 2)

def pentagonal(n):
    return n*(3*n - 1)/2

def is_pentagonal(n):
    return (n >= 1) and is_integer((1+sqrt(1+24*n))/6.0)

def hexagonal(n):
    return n*(2*n - 1)
       
def get_cardinal_name(num):
    """Get cardinal name for number (0 to 1 million)"""
    numbers = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
        15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty",
        50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
      }
    def _get_tens(n):
      a, b = divmod(n, 10)
      return (numbers[n] if (n in numbers) else "%s-%s" % (numbers[10*a], numbers[b]))    
    def _get_hundreds(n):
      tens = n % 100
      hundreds = (n / 100) % 10
      return list(compact([
        hundreds > 0 and numbers[hundreds], 
        hundreds > 0 and "hundred", 
        hundreds > 0 and tens and "and", 
        (not hundreds or tens > 0) and _get_tens(tens),
      ]))

    # This needs some refactoring
    if not (0 <= num < 1e6):
      raise ValueError, "value not supported: %s" % num      
    thousands = (num / 1000) % 1000
    strings = compact([
      thousands and (_get_hundreds(thousands) + ["thousand"]),
      (num % 1000 or not thousands) and _get_hundreds(num % 1000),
    ])
    return " ".join(flatten(strings))

def is_perfect(num):
    """Return -1 if num is deficient, 0 if perfect, 1 if abundant"""
    return cmp(sum(proper_divisors(num)), num)

def number_of_digits(num, base=10):
    """Return number of digits of num (expressed in base 'base')"""
    return int(log(num)/log(base)) + 1

def is_pandigital(digits, through=range(1, 10)):
    """Return True if digits form a pandigital number"""
    return (sorted(digits) == through)

# Decorators

def memoize(f, maxcache=None, cache={}):
    """Decorator to keep a cache of input/output for a given function"""
    cachelen = [0]
    def g(*args, **kwargs):
        key = (f, tuple(args), frozenset(kwargs.items()))
        if maxcache is not None and cachelen[0] >= maxcache:
            return f(*args, **kwargs)
        if key not in cache:
            cache[key] = f(*args, **kwargs)
            cachelen[0] += 1
        return cache[key]
    return g

class tail_recursive(object):
    """Tail recursive decorator."""
    # Michele Simionato's version 
    CONTINUE = object() # sentinel

    def __init__(self, func):
        self.func = func
        self.firstcall = True

    def __call__(self, *args, **kwd):
        try:
            if self.firstcall: # start looping
                self.firstcall = False
                while True:
                    result = self.func(*args, **kwd)
                    if result is self.CONTINUE: # update arguments
                        args, kwd = self.argskwd
                    else: # last call
                        break
            else: # return the arguments of the tail call
                self.argskwd = args, kwd
                return self.CONTINUE
        except: # reset and re-raise
            self.firstcall = True
            raise
        else: # reset and exit
            self.firstcall = True
            return result
        
class persistent(object):
    def __init__(self, it):
        self.it = it
        
    def __getitem__(self, x):
        self.it, temp = tee(self.it)
        if type(x) is slice:
            return list(islice(temp, x.start, x.stop, x.step))
        else:
            return islice(temp, x, x+1).next()
        
    def __iter__(self):
        self.it, temp = tee(self.it)
        return temp
