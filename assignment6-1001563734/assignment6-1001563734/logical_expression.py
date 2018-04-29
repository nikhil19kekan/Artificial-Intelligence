import sys
import copy
import re
#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
    """Prints the given expression using the given separator"""
    if expression == 0 or expression == None or expression == '':
        print '\nINVALID\n'

    elif expression.symbol[0]: # If it is a base case (symbol)
        sys.stdout.write('%s' % expression.symbol[0])

    else: # Otherwise it is a subexpression
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    word = ''
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Model is prefilled with symbols whose values are already known
def check_true_false(knowledge_base, statement,model):
    symbols = set()
    model1 = copy.deepcopy(model)
    symbols= getSymbols(knowledge_base,symbols)
    res1 = tt_check_all(knowledge_base,statement,symbols,model1)
    notstatement = logical_expression()
    notstatement.connective[0] = 'not'
    notstatement.subexpressions.append(statement)
    symbols = set()
    model2 = model
    symbols = getSymbols(knowledge_base,symbols)
    res2 = tt_check_all(knowledge_base,notstatement,symbols,model2)
    try:
	f = open('result.txt','w')
    except:
	sys.exit('Cannot open file')
    if res1 == True:
	if res2 == True:
    	    f.write('both true and false')
	    print('both true and false\n')
	else:
	    f.write('definitely true')
	    print('entails alpha\n');
    else:
	if res2 == True:
	    f.write('definitely false')
	    print('do not entails alpha\n')
	else:
	    f.write('possibly true or false')
	    print('possibly true or false\n')

# Getting all the symbols	
def getSymbols(kb,sym):
    for exp in kb.subexpressions:
	if exp.symbol[0]:
            sym.add(exp.symbol[0])
   	#if f=='':
	#    if re.match(r'^[P|M|B|S]_[1-4]_[1-4]$',exp.symbol[0]):
	#	model[exp.symbol[0]] = True
	#    elif exp.connective[0] == 'not' and re.match(r'^[P|M|B|S]_[1-4]_[1-4]$',exp.subexpressions[0].symbol[0]):
	#	model[exp.subexpressions[0].symbol[0]] = False  
	sym = getSymbols(exp,sym)  
    return sym

# The implementation of TT_Etails function that calls for only those symbols whose values are not known
def tt_check_all(kb,alpha,symbols,model):
	if len(symbols)==0:
	    #print('Before function call',model,symbols)
	    #print('kb1',checkPLTrue(kb,model))
	    #print(model)
            #print(eval(checkPLTrue(kb,model)))
	    if eval(checkPLTrue(kb,model)):
		#print('alpha1',eval(checkPLTrue(alpha,model)))
		return eval(checkPLTrue(alpha,model))
	    else:
		return True
	else:
	    p = symbols.pop()
	    while p in model and len(symbols)>0:
		p = symbols.pop()
		if p in model and len(symbols)==0:
		    #print('kb2',checkPLTrue(kb,model))
		    #print('h',model)
	            #print('alpha2',checkPLTrue(alpha,model))
		    #if eval(checkPLTrue(kb,model)):
	#		return eval(checkPLTrue(alpha,model))
	    	    #else:
		    return True
	    model1 = copy.deepcopy(model)
	    symbols1 = copy.deepcopy(symbols)
	    symbols2 = copy.deepcopy(symbols) 
	    model1[p] = True
	    call1 = tt_check_all(kb,alpha,symbols1,model1) 
	    #prinddt('model after true',model)
	    model[p] = False	
 	    call2 = tt_check_all(kb,alpha,symbols2,model)
	    #print('model after false',model)
	    return call1 and call2

# This is the evaluation function for evaluating the value of the model
def checkPLTrue(kb,model):
	exp = '('
	if re.match(r'^[P|M|B|S]_[1-4]_[1-4]$',kb.symbol[0]):   #Return the value of base symbol directly
	    return str(model[kb.symbol[0]])
	elif kb.connective[0] == 'and':				#Check if connective is 'and' recursively find value for all symbols
	    exp = '(True and '
	    for e in kb.subexpressions:
		exp += checkPLTrue(e,model)+' and '
	    exp = exp.strip(' and ')
	    exp = exp+')'
	    return exp
	elif kb.connective[0] == 'or':				
	    for e in kb.subexpressions:
	 	exp += checkPLTrue(e,model)+' or '
	    exp = exp.strip(' or ')
	    exp = exp+')'
	    return exp
	elif kb.connective[0] == 'not':
	    exp = '(not '+str(checkPLTrue(kb.subexpressions[0],model))+')'	
	    return exp
	elif kb.connective[0] == 'xor':				#Implementation for one and only one returns false if more than one symbols are true
	    c = 0
	    for e in kb.subexpressions:
		if checkPLTrue(e,model)=='True':
		    c+=1
	    if c>1:
		exp = 'False'	
	    else:
		exp = 'True'
	    return exp
	elif kb.connective[0] == 'if':
	    A = kb.subexpressions[0].symbol[0]
	    exp = '(not '+str(model[A])+' or '+checkPLTrue(kb.subexpressions[1],model)+')'
	    return exp
	elif kb.connective[0] == 'iff':
	    A = checkPLTrue(kb.subexpressions[0],model)
	    B = checkPLTrue(kb.subexpressions[1],model)
	    exp = '(not '+A+' or '+B+') and (not '+B+' or '+A+')'		              	
	    return exp
