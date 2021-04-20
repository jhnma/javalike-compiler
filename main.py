#!/usr/bin/env python3
from scannerDFA import getBOFToken, getEOFToken, TokenKind
import scanner
import lrparser
import sys

def main(fname = ""):
    try:
        f = open(fname, "r")
        code = f.read()
    except:
        print("File not found!")
        sys.exit(42)
    
    tokenListTuple = scanner.scanning(code)
    
    # scanning unsuccessful
    if tokenListTuple[1] == False:
        print("Error during scanning!")
        sys.exit(42)
    
    # Append BOF and EOF "$" symbol to list of tokens
    tokenList = [getBOFToken()] + tokenListTuple[0] + [getEOFToken()]
    tokenList = list(filter(lambda x: x.tokenType != TokenKind.COMMENT, tokenList))
    print(tokenList)
    # print(tokenList[-1].tokenType)

    parsedTuple = lrparser.parsing(tokenList)
    if parsedTuple[1] == False:
        print("Error during parsing!")
        # print(parsedTuple[0])
        sys.exit(42)
    
    parseTreeRoot = parsedTuple[0]
    recursivePrintParseTree(parseTreeRoot)

    print("Program accepted.")
    sys.exit(0)

def recursivePrintParseTree(rootNode, ident_level = 0):
    print(" " * ident_level, end = "")
    print(rootNode)
    if rootNode.isNonTerminal():
        for child in rootNode.children:
            recursivePrintParseTree(child, ident_level + 1)

if __name__ == "__main__":
    fname = sys.argv[1]
    main(fname)