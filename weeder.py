from parserDFA import NonTerminals
from scannerDFA import TokenKind
import astNodes

def weeder(parseTreeRoot):
    currentNode = parseTreeRoot.copy()
    assert parseTreeRoot.nonTerminal == NonTerminals.GOAL
    currentNode = parseTreeRoot.children[0] # COMPILATION_UNIT
    newAstNode = createRootNode(currentNode)
    
    # Do the weeding stuff

# Returns RootNode
def createRootNode(ptNode):
    if ptNode.nonTerminal == NonTerminals.COMPILATION_UNIT:
        package = []
        imports = []
        class_interface = None

        if ptNode.hasChildrenType(NonTerminals.PACKAGE_DECLARATION):
            packageNode = ptNode.getChildrenOfType(NonTerminals.PACKAGE_DECLARATION)[0]
            package = getName(packageNode.children[1])
        
        if ptNode.hasChildrenType(NonTerminals.IMPORT_DECLARATIONS):
            importsNode = ptNode.getChildrenOfType(NonTerminals.IMPORT_DECLARATIONS)[0]
            imports = getImports(importsNode)
        
        if ptNode.hasChildrenType(NonTerminals.TYPE_DECLARATION):
            typeNode = ptNode.getChildrenOfType(NonTerminals.TYPE_DECLARATION)[0]
            grandchild = typeNode.children[0]
            if grandchild.nonTerminal == NonTerminals.CLASS_DECLARATION:
                class_interface = createClassDeclNode(grandchild)
            elif grandchild.nonTerminal == NonTerminals.INTERFACE_DECLARATION:
                class_interface = createInterfaceDeclNode(grandchild)
            else:
                class_interface = None

        return astNodes.RootNode(package, imports, type)
    
    else:
        print("Error accessing a non-COMPILTAION_UNIT node")

# Returns [string] delimited by dot
def getName(ptNode):
    if ptNode.nonTerminal == NonTerminals.NAME:
        if ptNode.children[0].nonTerminal == NonTerminals.SIMPLE_NAME:
            return [ptNode.children[0].children[0].lexeme]
        else:
            return getName(ptNode.children[0].children[0]) + [ptNode.children[0].children[2].lexeme]
    else:
        print("Error accessing a non-NAME node")

# Returns [[string]]
def getImports(ptNode):
    if ptNode.nonTerminal == NonTerminals.IMPORT_DECLARATIONS:
        if len(ptNode.children) == 1:
            child = ptNode.children[0]
            if child.children[0].nonTerminal == NonTerminals.SINGLE_TYPE_IMPORT_DECLARATION:
                return [getName(child.children[0].children[1])]
            else:
                return [getName(child.children[0].children[1]) + ["*"]]
        else:
            child = ptNode.children[1]
            if child.children[0].nonTerminal == NonTerminals.SINGLE_TYPE_IMPORT_DECLARATION:
                c = [getName(child.children[0].children[1])]
            else:
                c = [getName(child.children[0].children[1]) + ["*"]]
            return getImports(ptNode.children[0]) + c
    else:
        print("Error accessing a non-IMPORT_DECLS node")

# Returns [[string]]
def getInterfaceNames(ptNode):
    if ptNode.nonTerminal == NonTerminals.INTERFACE_TYPE_LIST:
        if len(ptNode.children) == 1:
            return [getName(ptNode.children[0].children[0])]
        else:
            return getInterfaceNames(ptNode.children[0]) + [getName(ptNode.children[2].children[0])]

# Returns [astNodes.Modifiers]
def getModifiers(ptNode):
    dict = {
        TokenKind.KEYWORD_ABSTRACT: astNodes.Modifiers.ABSTRACT,
        TokenKind.KEYWORD_FINAL: astNodes.Modifiers.FINAL,
        TokenKind.KEYWORD_NATIVE: astNodes.Modifiers.NATIVE,
        TokenKind.KEYWORD_PROTECTED: astNodes.Modifiers.PROTECTED,
        TokenKind.KEYWORD_PUBLIC: astNodes.Modifiers.PUBLIC,
        TokenKind.KEYWORD_STATIC: astNodes.Modifiers.STATIC
    }
    if ptNode.nonTerminal == NonTerminals.MODIFIERS:
        if ptNode.children[0].nonTerminal == NonTerminals.MODIFIER:
            return [dict[ptNode.children[0].children[0].tokenType]]
        else:
            return getModifiers(ptNode.children[0]) + [dict[ptNode.children[1].children[0].tokenType]]

# Returns (astNodes.FieldType, [string])
def getDeclType(ptNode):
    if ptNode.isNonTerminal():
        if ptNode.tokenType == TokenKind.KEYWORD_VOID:
            return (astNodes.FieldType.VOID, ["void"])
    else:
        # NonTerminals.TYPE
        if ptNode.children[0].nonTerminal == NonTerminals.PRIMITIVE_TYPE:
            if ptNode.children[0].children[0].isTerminal():
                return (astNodes.FieldType.BOOLEAN, ["boolean"])
            else:
                dict = {
                    TokenKind.KEYWORD_BYTE: (astNodes.FieldType.BYTE, ["byte"]),
                    TokenKind.KEYWORD_SHORT: (astNodes.FieldType.SHORT, ["short"]),
                    TokenKind.KEYWORD_INT: (astNodes.FieldType.INT, ["int"]),
                    TokenKind.KEYWORD_CHAR: (astNodes.FieldType.CHAR, ["char"])
                }
                return dict[ptNode.children[0].children[0].children[0].children[0].tokenType]
        else:
            # REFERENCE_TYPE
            if ptNode.children[0].children[0].nonTerminal == NonTerminals.CLASS_OR_INTERFACE_TYPE:
                return (astNodes.FieldType.REFERENCE_TYPE, getName(ptNode.children[0].children[0].children[0]))
            else:
                if ptNode.children[0].children[0].children[0].nonTerminal == NonTerminals.PRIMITIVE_TYPE:
                    dict = {
                        TokenKind.KEYWORD_BYTE: (astNodes.FieldType.REFERENCE_TYPE, ["byte[]"]),
                        TokenKind.KEYWORD_SHORT: (astNodes.FieldType.REFERENCE_TYPE, ["short[]"]),
                        TokenKind.KEYWORD_INT: (astNodes.FieldType.REFERENCE_TYPE, ["int[]"]),
                        TokenKind.KEYWORD_CHAR: (astNodes.FieldType.REFERENCE_TYPE, ["char[]"])
                    }
                    return dict[ptNode.children[0].children[0].children[0].tokenType]
                else:
                    n = getName(ptNode.children[0].children[0].children[0])
                    n[-1] = n[-1] + "[]"
                    return (astNodes.FieldType.REFERENCE_TYPE, n)




def getExpression(ptNode):
    assert ptNode.nonTerminal == NonTerminals.EXPRESSION
    return getAssignmentExpression(ptNode.children[0])

def getAssignmentExpression(ptNode):
    assert ptNode.nonTerminal == NonTerminals.ASSIGNMENT_EXPRESSION
    if ptNode.children[0].nonTerminal == NonTerminals.CONDITIONAL_EXPRESSION:
        return getConditionalExpression(ptNode.children[0])
    else:
        return getAssignment(ptNode.children[0])

# def getConditionalExpression

def getAssignment(ptNode):
    assert ptNode.nonTerminal == NonTerminals.ASSIGNMENT
    lhs = ptNode.children[0]
    if lhs.children[0].nonTerminal == NonTerminals.NAME:
        lhs_ret = getName(lhs.children[0])
    elif lhs.children[0].nonTerminal == NonTerminals.FIELD_ACCESS:
        lhs
    else:






# def getBlockStmts(ptNode):




# def getArguments(ptNode)

# Returns ((astNodes.FieldType, [string]), string)
def getParams(ptNode):
    if ptNode.nonTerminal == NonTerminals.FORMAL_PARAMETER_LIST:
        if len(ptNode.children) == 1:
            return [getParam(ptNode.children[0])]
        else:
            return getParams(ptNode.children[0]) + [getParam(ptNode.children[2])]
    
    def getParam(pmNode):
        if pmNode.nonTerminal == NonTerminals.FORMAL_PARAMETER:
            return (getDeclType(pmNode.children[0]), pmNode.children[1].children[0].lexeme)

# Returns ClassDeclNode
def createClassDeclNode(ptNode):
    if ptNode.nonTerminal == NonTerminals.CLASS_DECLARATION:
        modifiers = getModifiers(ptNode.children[0])
        className = ptNode.children[2].lexeme
        extends = ["java", "lang", "Object"]
        implements = []

        if ptNode.hasChildrenType(NonTerminals.SUPER):
            extends = getName((ptNode.getChildrenOfType(NonTerminals.SUPER)[0].children)[1].children[0])
        
        if ptNode.hasChildrenType(NonTerminals.INTERFACES):
            implements = getInterfaceNames(ptNode.getChildrenOfType(NonTerminals.INTERFACES)[0][1])

        if ptNode.hasChildrenType(NonTerminals.CLASS_BODY):
            cbody_decls = ptNode.children[-1].children[1]
            ret = getAll(cbody_decls)
            fields = ret['fields']
            methods = ret['methods']
            constructors = ret['constructors']

            def getAll(cbdsNode):
                if cbdsNode.nonTerminal == NonTerminals.CLASS_BODY_DECLARATIONS:
                    if cbdsNode.children[0].nonTerminal == NonTerminals.CLASS_BODY_DECLARATION:
                        ret2 = getAll2(cbdsNode.children[0])
                    else:
                        ret2 = getAll(cbdsNode.children[0])
                        ret1 = getAll2(cbdsNode.children[1])
                        for ele in ret1:
                            if ele in ret2:
                                ret2[ele] = ret2[ele] + ret1[ele]
                            else:
                                ret2[ele] = ret1[ele]
                    return ret2
            
            def getAll2(cbdNode):
                if cbdNode.nonTerminal == NonTerminals.CLASS_BODY_DECLARATION:
                    if cbdNode.children[0].nonTerminal == NonTerminals.CLASS_MEMBER_DECLARATION:
                        cbdNodeC = cbdNode.children[0].children[0]
                        if cbdNodeC.nonTerminal == NonTerminals.FIELD_DECLARATION:
                            modifiers = getModifiers(cbdNodeC.children[0])
                            decl_type = getDeclType(cbdNodeC.children[1])
                            var_decltor = cbdNodeC.children[2]
                            var_id = var_decltor.children[0].children[0].lexeme
                            if len(var_decltor.children) == 1:
                                var_init = None
                            else:
                                var_init = getExpression(var_decltor.children[2].children[0])
                            return {'fields': [astNodes.Field(modifiers, decl_type, var_id, var_init)]}

                        else:
                            mheader = cbdNodeC.children[0]
                            modifiers = getModifiers(mheader.children[0])
                            ret_type = getDeclType(mheader.children[1])
                            method_id = mheader.children[2].children[0].lexeme

                            if mheader.children[2].hasChildrenType(NonTerminals.FORMAL_PARAMETER_LIST):
                                params = getParams(mheader.children[2].children[2])
                            else:
                                params = []

                            if cbdNodeC.children[1].children[0].isTerminal():
                                mbody = []
                            else:
                                if len(cbdNodeC.children[1].children[0].children) == 2:
                                    mbody = []
                                else:
                                    mbody = getBlockStmts(cbdNodeC.children[1].children[0].children[1]) # BlockStatement class
                            
                            return {'methods': [astNodes.Method(modifiers, ret_type, method_id, params, mbody)]}
                
                    else:
                        constructor = cbdNode.children[0]
                        modifiers = getModifiers(constructor.children[0])
                        if constructor.children[1].hasChildrenType(NonTerminals.FORMAL_PARAMETER_LIST):
                            params = getParams(constructor.children[1].children[2])
                        else:
                            params = []
                        
                        if constructor.children[2].hasChildrenType(NonTerminals.BLOCK_STATEMENTS):
                            cbody = getBlockStmts(constructor.children[2].children[1])
                        else:
                            cbody = []

                        return {'constructor': [astNodes.Constructor(modifiers, params, cbody)]}
        
        return astNodes.ClassDeclNode(className, modifiers, fields, constructors, methods, extends, implements)
    
    else:
        print("Error accessing a non-CLASS_DECL node")

def createInterfaceDeclNode(ptNode):
    if ptNode.nonTerminal == NonTerminals.INTERFACE_DECLARATION:
        modifiers = getModifiers(ptNode.children[0])
        interface_id = ptNode.children[2].lexeme

        if len(ptNode.children) == 5:
            extends = getExtInterfaces(ptNode.children[3])
        else:
            extends = []
        
        if ptNode.children[-1].hasChildrenType(NonTerminals.INTERFACE_MEMBER_DECLARATIONS):
            methods = getIMethods(ptNode.children[-1].children[1])

        else:
            intfBody = []
        
        return astNodes.InterfaceDeclNode(interface_id, modifiers, methods, extends)

    def getExtInterfaces(eiNode):
        if eiNode.nonTerminal == NonTerminals.EXTENDS_INTERFACES:
            if eiNode.children[0].isTerminal():
                return [getInterfaceType(eiNode.children[1])]
            else:
                return getExtInterfaces(eiNode.children[0]) + [getInterfaceType(eiNode.children[2])]
        
        def getInterfaceType(itfNode):
            if itfNode.nonTerminal == NonTerminals.INTERFACE_TYPE:
                return getName(itfNode.children[0].children[0])
    
    def getIMEthods(imdlNode):
        if imdlNode.nonTerminal == NonTerminals.INTERFACE_MEMBER_DECLARATIONS:
            if imdlNode.children[0].nonTerminal == NonTerminals.INTERFACE_MEMBER_DECLARATION:
                return [getIMethod(imdlNode.children[0])]
            else:
                return getIMethods(imdlNode.children[0]) + [getIMethod(imdlNode.children[1])]
        
        def getIMethod(imdNode):
            if imdNode.nonTerminal == NonTerminals.INTERFACE_MEMBER_DECLARATION:
                mheader = imdNode.children[0].children[0]
                modifiers = getModifiers(mheader.children[0])
                ret_type = getDeclType(mheader.children[1])
                mName = mheader.children[2].children[0].lexeme
                if mheader.children[2].hasChildrenType(NonTerminals.FORMAL_PARAMETER_LIST):
                    params = getParams(mheader.children[2].children[2])
                else:
                    params = []
                return astNodes.Method(modifiers, ret_type, mName, params, [])








# One function for each Non-Terminal (in general) / AST-class
# def createRootNode(parseTreeNode) -> AstNode (the root node):
    # assert parseTreeNode.nonTerminalType == NonTerminals.COMPILATION_UNIT
    # loop through children of the node, and call the functions for that type
    # def createPackageDecl(parseTreeNode) -> [string] (individual parts, no dots, ids)

# create a createName function because it appears in many places -> [strings]
