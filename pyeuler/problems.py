#!/usr/bin/python
import inspect
import sys
import re

from toolset import *

def problem1():
    """
    Add all the natural numbers below one thousand that are multiples of 3 or 5.
    """ 
    return sum(x for x in xrange(1, 1000) if x % 3 == 0 or x % 5 == 0)

def problem2():
    """
    Find the sum of all the even-valued terms in the Fibonacci sequence which 
    do not exceed four million.
    """
    even_fibonacci = (x for x in fibonacci() if x % 2)
    return sum(takewhile(lambda x: x < int(4e6), even_fibonacci))

### Main

def run_problem(problem_number, expected_results):
    """Run a problem and return True if result is successful."""
    function = globals()["problem%d" % problem_number]
    docstring = inspect.getdoc(function)
    result = function()
    expected_result = expected_results[problem_number]
    if result == expected_result: 
        status = "ok"
    else:
        status = "FAIL: expected %d but got %d" % (expected_result, result)
    print "%d: %s (%s)" % (problem_number, result, status)
    return (result == expected_result)

def main(args, expected_results):
    """Run Euler Project problems."""
    statuses = [run_problem(n, expected_results) for n in expected_results]    
    return (0 if all(statuses) else 1)

EXPECTED_RESULTS = {
    1: 233168,
    2: 4613732,
}


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:], EXPECTED_RESULTS))
