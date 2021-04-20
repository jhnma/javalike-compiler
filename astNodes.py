from scannerDFA import TokenKind
from enum import Enum

class Modifiers(Enum):
    ABSTRACT = TokenKind.KEYWORD_ABSTRACT
    FINAL = TokenKind.KEYWORD_FINAL
    NATIVE = TokenKind.KEYWORD_NATIVE
    PROTECTED = TokenKind.KEYWORD_PROTECTED
    PUBLIC = TokenKind.KEYWORD_PUBLIC
    STATIC = TokenKind.KEYWORD_STATIC

    def __str__(self):
        return self.name.lower()

class FieldType(Enum):
    BOOLEAN = TokenKind.KEYWORD_BOOLEAN
    BYTE = TokenKind.KEYWORD_BYTE
    CHAR = TokenKind.KEYWORD_CHAR
    INT = TokenKind.KEYWORD_INT
    SHORT = TokenKind.KEYWORD_SHORT
    VOID = TokenKind.KEYWORD_VOID
    REFERENCE_TYPE = 1000

    def __str__(self):
        return self.name.lower()
    
    def __repr__(self):
        return str(self)

class StatementType(Enum):
    EXPRESSION_STMT = 1
    IF = 2
    WHILE = 3
    FOR = 4
    RETURN = 5

    def __str__(self):
        return self.name.lower()

class AstNodeType(Enum):
    ROOT = 1
    PACKAGE = 2
    IMPORTS = 3
    CLASS = 4
    INTERFACE = 5
    CONSTRUCTOR = 6
    FIELD = 7
    METHOD = 8
    BLOCK = 9
    STATEMENT = 10
    EXPRESSION = 11

class ExpressionType(Enum):
    LITERAL = 1
    KEYWORD = 2
    PARENTHESIZED = 3
    CLASS_INSTANCE_CREATION = 4
    ARRAY_CREATION = 5
    FIELD_ACCESS = 6
    METHOD_INVOCATION = 7
    ARRAY_ACCESS = 8
    CAST = 9
    UNARY = 10
    BINARY = 11
    ASSIGNMENT = 12

    # Binary ones
    # MULTIPLICATIVE = 9
    # ADDITIVE = 10
    # RELATIONAL = 11
    # LOGICAL = 12      # Eager
    # CONDITIONAL = 13  #Lazy eval
    # ASSIGNMENT = 14

def isParams(params):
    assert isinstance(params, list)
    for param in params:
        assert isinstance(param, tuple)
        assert isinstance(param[0], tuple)
        assert isinstance(param[0][0], FieldType)
        assert isinstance(param[0][1], list)
        for p in param[0][1]:
            assert isinstance(p, str)
        assert isinstance(param[1], str)
    return True

def isModifiers(mods):
    assert isinstance(mods, list)
    for mod in mods:
        assert isinstance(mod, Modifiers)
    return True

def isName(namelst):
    assert isinstance(namelst, list)
    for n in namelst:
        assert isinstance(n, str)

class AstNode:
    def __init__(self):
        self.nodeType = None

class RootNode(AstNode):
    # package: [string], imports: [[string]], class_dec: ClassInterfaceDeclNode
    def __init__(self, package, imports, class_interface):

        def typeCheck():
            isName(package)
            assert isinstance(imports, list)
            for imp in imports:
                isName(imp)
            assert isinstance(class_dec, ClassInterfaceDeclNode)

        typeCheck()
        self.nodeType = AstNodeType.ROOT
        self.package = package
        self.imports = imports
        self.class_interface = class_interface

class ClassInterfaceDeclNode(AstNode):
    def isClass(self):
        return False
    
    def isInterface(self):
        return False

class ClassDeclNode(ClassInterfaceDeclNode):
    # name: string, modifiers: [Modifiers], fields: [Field], methods: [Method], constructors: [Constructor]
    # superclass: [string], interfaces: [[string]]
    # Superclass: Java.lang.object by default
    def __init__(self, name, class_modifiers, fields, constructors, methods, superclass, interfaces):

        def typeCheck():
            assert isinstance(name, str)
            isModifiers(class_modifiers)
            assert isinstance(fields, list)
            for field in fields:
                assert isinstance(field, Field)
            assert isinstance(constructors, list)
            for constructor in constructors:
                assert isinstance(constructor, Constructor)
            assert isinstance(methods, list)
            for method in methods:
                assert isinstance(method, Method)
            isName(superclass)
            assert isinstance(interfaces, list)
            for interface in interfaces:
                isName(interface)

        typeCheck()
        self.nodeType = AstNodeType.CLASS
        self.name = name
        self.modifiers = class_modifiers
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        self.superclass = superclass
        self.interfaces = interfaces

class InterfaceDeclNode(AstNode):
    # name: string, modifiers: [Modifiers], methods: [Method], interfaces: [[string]]
    def __init__(self, name, modifiers, methods, interfaces = []):

        def typeCheck():
            assert isinstance(name, str)
            isModifiers(modifiers)
            assert isinstance(methods, list)
            for method in methods:
                assert isinstance(method, Method)
            assert isinstance(interfaces, list)
            for interface in interfaces:
                isName(interface)
        
        typeCheck()
        self.name = name
        self.modifiers = modifiers
        self.methods = methods
        self.superinterfaces = superinterfaces
        self.nodeType = AstNodeType.INTERFACE
    
    def isInterface(self):
        return True

class Field(AstNode):
    # modifiers: [Modifiers], decl_type: FieldType, identifier: string, initialization: Expression
    def __init__(self, modifiers, decl_type, identifier, initialization):

        def typeCheck():
            isModifiers(modifiers)
            assert isinstance(decl_type, FieldType)
            assert isinstance(identifier, str)
            assert isinstance(initialization, Expression)

        typeCheck()
        self.nodeType = AstNodeType.FIELD
        self.modifiers = modifiers
        self.type = decl_type
        self.identifier = identifier
        self.init = initialization

class Statement(AstNode):
    def __init__(self):
        self.nodeType = AstNodeType.STATEMENT

class BlockStatement(Statement):
    def __init__(self):
        self.nodeType = AstNodeType.STATEMENT

    def __repr__(self):
        return "BlockStmt <>"

class Method(AstNode):
    # modifiers: [Modifiers], type: FieldType, identifier: string, params: [((FieldType, [str]), str)], body: BlockStatement
    def __init__(self, modifiers, return_type, identifier, params, body):

        def typeCheck():
            isModifiers(modifiers)
            assert isinstance(return_type, FieldType)
            assert isinstance(identifier, str)
            isParams(params)
            assert isinstance(body, BlockStatement)
            return True

        typeCheck()
        self.nodeType = AstNodeType.METHOD
        self.modifiers = modifiers
        self.type = return_type
        self.identifier = identifier
        self.params = params
        self.body = body
    
    def __repr__(self):
        return "Method <modifiers: %s, type: \"%s\", identifier: \"%s\", params: %s, body: %s>" % (list(map(lambda x: str(x) ,self.modifiers)), str(self.type), self.identifier, self.params, self.body)

class Constructor(AstNode):
    def __init__(self, modifiers, params, body):

        def typeCheck():
            assert isModifiers(modifiers)
            assert isParams(params)
            assert isinstance(body, BlockStatement)
            return True
        
        assert typeCheck()
        self.nodeType = AstNodeType.CONSTRUCTOR
        self.modifiers = modifiers
        self.params = params
        self.body = body

# class VarDeclStatement(Statement):
#     #            LOCAL_VARIABLE_DECLARATION -> TYPE, VARIABLE_DECLARATOR_ID, operator_equals, VARIABLE_INITIALIZER

# class 



# some exprs can be a statement, make expr a subclass of statement

# STATEMENT_EXPRESSION -> ASSIGNMENT
#     ASSIGNMENT -> LEFT_HAND_SIDE, ASSIGNMENT_OPERATOR, ASSIGNMENT_EXPRESSION
#         ASSIGNMENT_OPERATOR -> operator_equals
#         ASSIGNMENT_EXPRESSION -> CONDITIONAL_EXPRESSION (see expressions)
#         ASSIGNMENT_EXPRESSION -> ASSIGNMENT
# STATEMENT_EXPRESSION -> METHOD_INVOCATION (calling )
#     METHOD_INVOCATION -> NAME, left_parenthesis, right_parenthesis
#     METHOD_INVOCATION -> NAME, left_parenthesis, ARGUMENT_LIST, right_parenthesis
#     METHOD_INVOCATION -> PRIMARY, dot, identifier, left_parenthesis, right_parenthesis
#     METHOD_INVOCATION -> PRIMARY, dot, identifier, left_parenthesis, ARGUMENT_LIST, right_parenthesis
#         ARGUMENT_LIST -> EXPRESSION
#         ARGUMENT_LIST -> ARGUMENT_LIST, comma, EXPRESSION
# STATEMENT_EXPRESSION -> CLASS_INSTANCE_CREATION_EXPRESSION
#     CLASS_INSTANCE_CREATION_EXPRESSION -> keyword_new, CLASS_TYPE, left_parenthesis, right_parenthesis
#     CLASS_INSTANCE_CREATION_EXPRESSION -> keyword_new, CLASS_TYPE, left_parenthesis, ARGUMENT_LIST, right_parenthesis
#         CLASS_TYPE -> CLASS_OR_INTERFACE_TYPE
#             CLASS_OR_INTERFACE_TYPE -> NAME

# class ExprStatement(Statement):
#     def __init__(self):
#         self.

class IfStatement(Statement):
    def __init__(self, cond_expr, if_true_stmt, if_false_stmt = []):
        self.if_cond = cond_expr
        self.if_true_body = if_true_stmt
        self.if_false_body = if_false_stmt

class WhileStatement(Statement):
    def __init__(self, cond_expr, stmt):
        self.while_cond = cond_expr
        self.while_body = stmt

class ForStatement(Statement):
    def __init__(self, init, expr, update, stmt):
        self.for_init = init
        self.for_term_cond = expr
        self.for_update = update
        self.for_body = stmt

class ReturnStatement(Statement):
    def __init__(self, expr):
        self.ret_expr = expr

class Expression(AstNode):
    def __init__(self):
        self.type = None

# class classInstanceCreationExpr(Expression):
#     def __init__(self, class_type, args):
#         self.type = 


# class UnaryExpression(Expression):
    # fields: one operator and one operand














if __name__ == "__main__":
    method_example = Method([Modifiers.PUBLIC], FieldType.INT, "hello_world", [((FieldType.BOOLEAN, ["boolean"]), "x")], BlockStatement())
    assert isinstance(method_example, Method)
    print(method_example)