from parserDFA import NonTerminals, getProductionRules, getReduceDFA, getShiftDFA
from scannerDFA import ParseTreeNode

shift_dfa = getShiftDFA()
reduce_dfa = getReduceDFA()
production_rules = getProductionRules()

# Input: List of tokens from the scanner
# Output: Root of the Parse Tree Node, or failure
def parsing(tokens):
    stack = []

    for token in tokens:
        while reduce(stack, token) != []:
            rule = reduce(stack, token)
            children = []
            for i in range(len(rule[1])):
                child = stack.pop()
                children.append(child)
            stack.append(NonTerminalNode(rule[0], children)) # put a tree node instead of symbol
        
        if reject(stack + [token]):
            return (stack, False)
        
        stack.append(token)
    
    # Stack is in the form [BOF, Goal, EOF]
    # BOF keeps the state stack and node stack in the same length
    # EOF ($) keeps token unempty
    return (stack[1], True)

# TODO: accept comments in parsing


# Reduce(stack, a) := { A -> gamma : exists beta. alpha = [beta,gamma] and [beta,A,a] is V.P. }
def reduce(stack, token):
    current_state = 0

    for symbol in stack:
        if symbol.isTerminal():
            id = symbol.tokenType
        else:
            id = symbol.nonTerminal
        try:
            current_state = shift_dfa[current_state][id]
        except:
            return []
    
    if current_state in reduce_dfa:
        if token.tokenType in reduce_dfa[current_state]:
            return production_rules[reduce_dfa[current_state][token.tokenType]]
        else:
            return []
    else:
        return []

# Reject(a) := ( a is not a V.P. )
def reject(inp):
    current_state = 0

    for symbol in inp:
        if symbol.isTerminal():
            id = symbol.tokenType
        else:
            id = symbol.nonTerminal
        
        # print(id)

        try:
            current_state = shift_dfa[current_state][id]
        except:
            return True
    
    return False

class NonTerminalNode(ParseTreeNode):
    def __init__(self, nonTerminal, children):
        self.nonTerminal = nonTerminal
        self.children = children

    def isNonTerminal(self):
        return True
    
    def __repr__(self):
        return "NonTerminal <nonTerminalType: \"%s\", children: %s>" % (self.nonTerminal, list(map(printTreeChildren, self.children)))
    
    def hasChildrenType(self, nonTerminalType):
        return nonTerminalType in list(map(lambda x: x.nonTerminal, self.children))

    def getChildrenOfType(self, nonTerminalType):
        return list(filter(lambda x: x.nonTerminal == nonTerminalType, self.children))

def printTreeChildren(child):
    if child.isTerminal():
        return str(child.tokenType)
    else:
        return str(child.nonTerminal)
