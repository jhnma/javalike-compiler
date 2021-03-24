from scannerDFA import getBOFToken, getEOFToken
import scanner
import lrparser

def main(fname = ""):
    try:
        f = open(fname, "r")
        code = f.read()
    except:
        print("File not found!")
        return 42
    
    tokenListTuple = scanner.scanning(code)
    
    # scanning unsuccessful
    if tokenListTuple[1] == False:
        print("Error during scanning!")
        print("\".")
        return 42
    
    # Append BOF and EOF "$" symbol to list of tokens
    tokenList = [getBOFToken()] + tokenListTuple[0] + [getEOFToken()]
    print(tokenList)
    # print(tokenList[-1].tokenType)

    parsedTuple = lrparser.parsing(tokenList)
    if parsedTuple[1] == False:
        print("Error during parsing!")
        print(parsedTuple[0])
        return 42
    
    parseTreeRoot = parsedTuple[0]
    print(parseTreeRoot)

    return 0

if __name__ == "__main__":
    # fname = input()
    fname = "J1_01.java"
    main(fname)