#!/usr/bin/python
"""
Run Project Euler problems in functional-programming style.

    $ wget http://projecteuler-solutions.googlecode.com/svn/trunk/Solutions.txt
    
    $ python pyeuler/run.py --solutions-file Solutions.txt 
    1: 233168 (ok)
    2: 4613732 (ok)

Author: Arnau Sanchez <tokland@gmail.com>
Website: http://github.com/tokland/pyeuler
"""
import optparse
import inspect
import sys
import re

import problems

def run_problem(number, function, solutions=None):
    """Run a problem and return True if result is successful."""
    docstring = inspect.getdoc(function)
    result = function()
    if solutions:
        solution = solutions[number]
        status = ("ok" if result == solution else 
            "FAIL: expected solution is %s" % solution)
        print "%d: %s (%s)" % (number, result, status)
        return (result == solution)
    else:
        print "%d: %s" % (number, result)

def parse_solutions(lines, format="^(?P<num>\d+)\.\s+(?P<solution>\w+)$"):
    """Yield pairs (problem_number, solution) parsing from lines."""
    re_format = re.compile(format)
    for line in lines:
        match = re_format.match(line.rstrip())
        if match:
            num, solution = int(match.group("num")), match.group("solution")
            solution2 = (int(solution) if solution.isdigit() else solution)
            yield num, solution2 

def main(args):
    """Run Project Euler problems."""
    usage = """%prog [OPTIONS] [N1 [N2 ...]]

    Run Project Euler problems.""" 
    parser = optparse.OptionParser(usage)
    parser.add_option('-s', '--solutions-file', dest='solutions_file',
        default=None, metavar="FILE", type="string", help='Solutions file')
    options, args0 = parser.parse_args(args)
    tosolve = map(int, args0)
    solutions = (options.solutions_file and 
        dict(parse_solutions(open(options.solutions_file))))
    problem_functions = dict((int(re.match("problem(\d+)$", s).group(1)), fun) 
        for (s, fun) in inspect.getmembers(problems) if s.startswith("problem"))
    statuses = [run_problem(num, fun, solutions) for (num, fun) in 
        sorted(problem_functions.iteritems()) if not tosolve or num in tosolve]
    return (0 if all(statuses) else 1)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
