from scannerDFA import TokenKind

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
            stack.append(NonTerminalsNode(rule[0], children)) # put a tree node instead of symbol
        
        if reject(stack + a):
            return (stack, False)
        
        stack.append(token)
    
    # Stack is in the form [BOF, Goal, EOF]
    # BOF keeps the state stack and node stack in the same length
    # EOF ($) keeps token unempty
    return (stack[1], True)

def reduce(stack, token):

    # Reduce(stack, a) := {A -> γ : exists β. α = βγ and βAa is V.P. }
    # Run the stack list on the parserDFA
    # If throws error, not a V.P.
    # Choose the state's rule that has lookahead symbol of token
    # If that rule indicates "shift", return []
    # If that rule indicates "reduce", return the corresponding reduction rule
    # only need shifting to run th estack, check it on the reduce dfa with the token

def reject(inp):
    # Reject(α) := ( α is not a V.P. )
    # Run the inp string on the parserDFA
    # If throws error, not a V.P., return True
    # If not, it is a valid V.P., return False
    # only needs shifitng  dfa

class ParseTreeNode:
    def isTerminal():
        return False

    def isNonTerminal():
        return False

class NonTerminalNode(ParseTreeNode)
    nonterminal enum
    list of children

    def isNonTerminal():
        return True







class parserdfanode # equiv to states
    id
    hasDotInEnd # having 1 makes this field true
    list of production rules that have the dot in the end

parserDFA variable that is nested dictionary

production rules: [(<Non-terminal>, [<non-terminals union terminals>])]
# terminals can just adopt the tokenkind
# non-terminals can have a second enum


record production rule when the 


# parser returns parse tree node, write a func that returns the AST node given a parse tree node
# reductions: amend the stack and perform dfa on the stack
# shifts: transitions of dfa