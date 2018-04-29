#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
from logical_expression import *


def main(argv):
    if len(argv) != 4:
        print 'Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' \
            % argv[0]
        sys.exit(0)

    # Read wumpus rules file

    try:
        input_file = open(argv[1], 'rb')
    except:
        print 'failed to open file %s' % argv[1]
        sys.exit(0)

    # Create the knowledge base with wumpus rules

    print '\nLoading wumpus rules...'
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:

        # Skip comments and blank lines. Consider all line ending types.

        if line[0] == '#' or line == '\r\n' or line == '\n' or line \
            == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()

    # Read additional knowledge base information file

    try:
        input_file = open(argv[2], 'rb')
    except:
        print 'failed to open file %s' % argv[2]
        sys.exit(0)

    # Model is created here to get the additional knowledge for the optimization process....

    model = {}

    # Add expressions to knowledge base

    print '\nLoading additional knowledge...'
    for line in input_file:

        # Skip comments and blank lines. Consider all line ending types.

        if line[0] == '#' or line == '\r\n' or line == '\n' or line \
            == '\r':
            continue
        counter = [0]  # a mutable counter
        l = line.rstrip('\r\n')
        subexpression = read_expression(l, counter)
        knowledge_base.subexpressions.append(subexpression)
        if re.search('not ', l):
            p = re.search('[M|P|S|B]_[1-4]_[1-4]', l)
            model[p.group(0)] = False
        else:
            model[l] = True
    input_file.close()
    print model

    # Verify it is a valid logical expression

    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # I had left this line out of the original code. If things break, comment out.

    print_expression(knowledge_base, '\n')

    # Read statement whose entailment we want to determine

    try:
        input_file = open(argv[3], 'rb')
    except:
        print 'failed to open file %s' % argv[3]
        sys.exit(0)
    print '\nLoading statement...'
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()

    # Convert statement into a logical expression and verify it is valid

    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is

    print 'Checking statement: ',
    print_expression(statement, '')
    print '\n'

    # Run the statement through the inference engine

    check_true_false(knowledge_base, statement, model)

    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)