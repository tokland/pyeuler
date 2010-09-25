#!/usr/bin/python
"""
Run Project Euler problems in functional-programming style.

    $ wget http://projecteuler-solutions.googlecode.com/svn/trunk/Solutions.txt
    
    $ python run.py --solutions-file Solutions.txt 
    1: 233168 (ok) in 0.0002 seconds
    2: 4613732 (ok) in 0.0001 seconds
    ...

    $ python run.py --solutions-file Solutions.txt 1 5 9 
    1: 233168 (ok) in 0.0002 seconds
    5: 232792560 (ok) in 0.0000 seconds
    9: 31875000 (ok) in 0.1019 seconds

Author: Arnau Sanchez <tokland@gmail.com>
Website: http://github.com/tokland/pyeuler
"""
import optparse
import inspect
import time
import sys
import re

import problems

def run_problem(number, function, solutions=None):
    """Run a problem and return boolean state (None if no solution available)."""
    docstring = inspect.getdoc(function)
    itime = time.time()
    result = function()
    elapsed = time.time() - itime
    if solutions:
        solution = solutions[number]
        status = ("ok" if result == solution else 
            "FAIL: expected solution is %s" % solution)
        print "%d: %s (%s) in %0.4f seconds" % (number, result, status, elapsed)
        return (result == solution)
    else:
        print "%d: %s in %0.4f seconds" % (number, result, elapsed)

def parse_solutions(lines, format="^(?P<num>\d+)\.\s+(?P<solution>\S+)$"):
    """Yield pairs (problem_number, solution) parsed from lines."""
    re_format = re.compile(format)
    for line in lines:
        match = re_format.match(line.rstrip())
        if match:
            num, solution = int(match.group("num")), match.group("solution")
            solution2 = (int(solution) if re.match("[\d-]+$", solution) else solution)
            yield num, solution2 

def main(args):
    """Run Project Euler problems."""
    usage = """%prog [OPTIONS] [N1 [N2 ...]]

    Run solutions to Project Euler problems.""" 
    parser = optparse.OptionParser(usage)
    parser.add_option('-s', '--solutions-file', dest='solutions_file',
        default=None, metavar="FILE", type="string", help='Solutions file')
    options, args0 = parser.parse_args(args)
    
    solutions = (options.solutions_file and 
        dict(parse_solutions(open(options.solutions_file))))
    tosolve = map(int, args0)
    problem_functions = dict((int(re.match("problem(\d+)$", s).group(1)), fun) 
        for (s, fun) in inspect.getmembers(problems) if s.startswith("problem"))
        
    itime = time.time()
    statuses = [run_problem(num, fun, solutions) for (num, fun) in 
        sorted(problem_functions.iteritems()) if not tosolve or num in tosolve]
    elapsed = time.time() - itime
    ps = "problem" + ("" if len(statuses) == 1 else "s")    
    print "--- %d %s run (%d failed) in %0.4f seconds" % \
      (len(statuses), ps, statuses.count(False), elapsed) 
    return (0 if all(statuses) else 1)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
