#!/usr/bin/python
"""
Run Project Euler problems in functional-programming style.

Get a solutions file here (note: I am not the owner this site):
    
http://projecteuler-solutions.googlecode.com/svn/trunk/Solutions.txt

Author: Arnau Sanchez <tokland@gmail.com>
"""
import optparse
import inspect
import sys
import re

import problems

def run_problem(name, function, solutions=None):
    """Run a problem and return True if result is successful."""
    number = int(re.match("problem(\d+)($|_)", name).group(1))
    docstring = inspect.getdoc(function)
    result = function()
    if solutions:
        solution = solutions[number]
        status = ("ok" if result == solution else 
            "FAIL: solution was %d but returned %d" % (solution, result))
        print "%d: %s (%s)" % (number, result, status)
        return (result == solution)
    else:
        print "%d: %s" % (number, result)

def parse_solutions(lines, format="^(?P<id>\d+)\.\s+(?P<solution>\w+)$"):
    """Parse lines to get solutions using given format regular expression."""
    re_format = re.compile(format)
    for line in lines:
        match = re_format.match(line.rstrip())
        if match:
            idnum, solution = int(match.group("id")), match.group("solution")
            solution2 = (int(solution) if solution.isdigit() else solution)
            yield idnum, solution2 

def main(args):
    """Run Euler Project problems."""
    usage = """%prog [OPTIONS] [N1 [N2 ...]]

    Run Pyeuler problems.""" 
    parser = optparse.OptionParser(usage)
    parser.add_option('-s', '--solutions-file', dest='solutions_file',
        default=None, metavar="FILE", type="string", help='Solutions file')
    options, args0 = parser.parse_args(args)
    solutions = (options.solutions_file and 
        dict(parse_solutions(open(options.solutions_file))))
    problem_functions = dict((s, fun) for (s, fun) in 
        inspect.getmembers(problems) if s.startswith("problem"))
    statuses = [run_problem(name, fun, solutions) for (name, fun) in 
        sorted(problem_functions.iteritems())]    
    return (0 if all(statuses) else 1)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
