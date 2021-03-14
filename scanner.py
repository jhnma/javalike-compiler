from scannerDFA import TokenKind
from scannerDFA import DfaNode
from scannerDFA import Token
from scannerDFA import getDfa
from scannerDFA import getReservedWords
import copy

# Input: source code in ASCII string, Output: list of Tokens representing the input string
def scanning(code):
    dfa = getDfa()
    reservedWords = getReservedWords()
    code_list = list(code)
    token_list = []
    line_terminators = ["\n", "\r", "\r\n"]
    spaces = [" ", "\t", "\f"] + line_terminators

    while code_list:
        current_lexeme = ""
        last_accepting_state = None
        last_accepting_lexeme = ""
        current_state = DfaNode("start", False)

        while True:
            try:
                character = code_list[0]
                print("\"", list(character), "\"")
                current_state = dfa[current_state][character]
                code_list.pop(0)
                current_lexeme = current_lexeme + character
                print("lexeme updated:", current_lexeme)
                print(current_state)
                print(current_state.isAccepting)
                if current_state.isAccepting:
                    last_accepting_state = copy.deepcopy(current_state)
                    last_accepting_lexeme = current_lexeme
            except:
                break

        print(current_lexeme)
        print(last_accepting_lexeme)
        print(last_accepting_state)
        print("Yes")

        if last_accepting_lexeme == "" and last_accepting_state is None:
            return (token_list, False) # returns token_list of work done, but error occurs (indicated by False)

        if current_lexeme in reservedWords:
            token_kind = reservedWords[current_lexeme]
        else:
            token_kind = last_accepting_state.tokenType

        if (character in spaces) or (character in line_terminators):
            code_list.pop(0)
            try:
                front_char = code_list[0]
                while front_char in spaces or front_char in line_terminators:
                    code_list.pop(0)
                    front_char = code_list[0]
            except:
                pass
        
        token_list.append(Token(last_accepting_lexeme, token_kind))
    
    return (token_list, True)


# Testing zone
f = open("J1_01.java", "r")
code = f.read()
# print(list(code))
tl = scanning(code)
print(tl)