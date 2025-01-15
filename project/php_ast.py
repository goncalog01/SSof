import enum


class AstNodeType(enum.Enum):
    STATEMENT_EXPRESSION = 1
    EXPRESSION_ASSIGN = 2
    EXPRESSION_VARIABLE = 3
    SCALAR = 4
    EXPRESSION_FUNCTION_CALL = 5
    ARGUMENT = 6
    STATEMENT_NOP = 7
    STATEMENT_IF = 8
    PROGRAM = 9
    STATEMENT_WHILE = 10
    EXPRESSION_BINARY = 11
    STATEMENT_ELSE = 12
    STATEMENT_BREAK = 13
    EXPRESSION_PRE_INC = 14
    EXPRESSION_POST_INC = 15
    EXPRESSION_CONST_FETCH = 16
    STATEMENT_ECHO = 17  # TODO
    STATEMENT_CONTINUE = 18  # TODO
    EXPRESSION_ASSIGN_OP = 19
    EXPRESSION_ARRAY_DIM_FETCH = 20
    EXPRESSION_BITWISE_NOT = 21
    EXPRESSION_BOOLEAN_NOT = 22
    STATEMENT_ELSEIF = 23
    EXPRESSION_PRINT = 24
    EXPRESSION_UNARY = 24

    @staticmethod
    def match(node_type: str):  # -> AstNodeType: # type: ignore
        if node_type == "Stmt_Expression":
            return AstNodeType.STATEMENT_EXPRESSION
        elif node_type == "Expr_Assign":
            return AstNodeType.EXPRESSION_ASSIGN
        elif node_type == "Expr_Variable":
            return AstNodeType.EXPRESSION_VARIABLE
        elif node_type == "Expr_FuncCall":
            return AstNodeType.EXPRESSION_FUNCTION_CALL
        elif node_type == "Arg":
            return AstNodeType.ARGUMENT
        elif node_type == "Stmt_Nop":
            return AstNodeType.STATEMENT_NOP
        elif "Scalar" in node_type:
            return AstNodeType.SCALAR
        elif "Expr_BinaryOp_" in node_type:
            return AstNodeType.EXPRESSION_BINARY
        elif node_type == "Stmt_If":
            return AstNodeType.STATEMENT_IF
        elif node_type == "Stmt_While":
            return AstNodeType.STATEMENT_WHILE
        elif node_type == "Stmt_Else":
            return AstNodeType.STATEMENT_ELSE
        elif node_type == "Stmt_Break":
            return AstNodeType.STATEMENT_BREAK
        elif node_type == "Expr_ConstFetch":
            return AstNodeType.EXPRESSION_CONST_FETCH
        elif node_type == "Expr_PostInc":
            return AstNodeType.EXPRESSION_POST_INC
        elif node_type == "Expr_PreInc":
            return AstNodeType.EXPRESSION_PRE_INC
        elif node_type == "Expr_PreDec":
            return AstNodeType.EXPRESSION_PRE_INC # for our use case its the same as increments
        elif node_type == "Expr_PostDec":
            return AstNodeType.EXPRESSION_POST_INC
        elif "Expr_AssignOp" in node_type:
            return AstNodeType.EXPRESSION_ASSIGN_OP
        elif node_type == "Expr_ArrayDimFetch":
            return AstNodeType.EXPRESSION_ARRAY_DIM_FETCH
        elif node_type == "Expr_BooleanNot":
            return AstNodeType.EXPRESSION_BOOLEAN_NOT
        elif node_type == "Expr_BitwiseNot":
            return AstNodeType.EXPRESSION_BITWISE_NOT
        elif node_type == "Stmt_ElseIf":
            return AstNodeType.STATEMENT_ELSEIF
        elif node_type == "Stmt_Echo":
            return AstNodeType.STATEMENT_ECHO
        elif node_type == "Stmt_Continue":
            return AstNodeType.STATEMENT_CONTINUE
        elif node_type == "Expr_Print":
            return AstNodeType.EXPRESSION_PRINT
        elif "Expr_Unary" in node_type:
            return AstNodeType.EXPRESSION_UNARY
        else:
            raise ValueError(f"Invalid Type {node_type}")


class AstNode:

    __anonymous_var_counter = 0

    @staticmethod
    def make_program_node(json_l: list):
        node = AstNode(AstNodeType.PROGRAM)
        node.statements = [AstNode.make_node(n) for n in json_l]
        if node.statements[-1]._type == AstNodeType.STATEMENT_NOP:
            node.statements.pop()
        return node

    @staticmethod
    def make_node(json_d: dict):
        node = AstNode(AstNodeType.match(json_d["nodeType"]))
        if node._type == AstNodeType.STATEMENT_EXPRESSION:
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.EXPRESSION_ASSIGN:
            node.var = AstNode.make_node(json_d["var"])
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.SCALAR:
            node.value = json_d["value"]
        elif node._type == AstNodeType.EXPRESSION_FUNCTION_CALL:
            node.name = '.'.join(json_d["name"]["parts"])
            node.args = [AstNode.make_node(node) for node in json_d["args"]]
        elif node._type == AstNodeType.ARGUMENT:
            node.name = json_d["name"]
            node.value = AstNode.make_node(json_d["value"])
        elif node._type == AstNodeType.EXPRESSION_VARIABLE:
            node.name = '$' + json_d["name"]
        elif node._type == AstNodeType.EXPRESSION_BINARY:  # hack to give types to the loops
            node.left = AstNode.make_node(json_d["left"])
            node.right = AstNode.make_node(json_d["right"])
        elif node._type == AstNodeType.STATEMENT_IF:
            # simple process to discover implicit flows
            var_node = AstNode(AstNodeType.EXPRESSION_VARIABLE)
            var_node.name = f"__anon__{AstNode.__anonymous_var_counter}"
            AstNode.__anonymous_var_counter += 1
            expr_assign = AstNode(AstNodeType.EXPRESSION_ASSIGN)
            expr_assign.var = var_node
            expr_assign.expr = AstNode.make_node(json_d["cond"])
            node.condition = expr_assign
            node.statements = [
                AstNode.make_node(node) for node in json_d["stmts"]
            ]
            current = node
            backup = current
            for n in json_d["elseifs"]:
                current.else_ = AstNode(AstNodeType.STATEMENT_ELSE)
                current.else_.statements = [AstNode.make_node(n)]
                current = current.else_
            
            current.else_ = AstNode.make_node(
                json_d["else"]) if json_d["else"] else None
            
            node = backup

        elif node._type == AstNodeType.STATEMENT_ELSEIF:
            node._type = AstNodeType.STATEMENT_IF
            var_node = AstNode(AstNodeType.EXPRESSION_VARIABLE)
            var_node.name = f"__anon__{AstNode.__anonymous_var_counter}"
            AstNode.__anonymous_var_counter += 1
            expr_assign = AstNode(AstNodeType.EXPRESSION_ASSIGN)
            expr_assign.var = var_node
            expr_assign.expr = AstNode.make_node(json_d["cond"])
            node.condition = expr_assign
            node.statements = [
                AstNode.make_node(node) for node in json_d["stmts"]
            ]
            node.else_ = None
        elif node._type == AstNodeType.STATEMENT_ECHO:
            node._type = AstNodeType.STATEMENT_EXPRESSION
            function_node = AstNode(AstNodeType.EXPRESSION_FUNCTION_CALL)
            function_node.name = "echo"
            function_node.args = [AstNode(AstNodeType.ARGUMENT) for _ in json_d["exprs"]]
            for i, n in enumerate(json_d["exprs"]):
                function_node.args[i].value = AstNode.make_node(n)
            node.expr = function_node
        elif node._type == AstNodeType.EXPRESSION_PRINT:
            function_node = AstNode(AstNodeType.EXPRESSION_FUNCTION_CALL)
            function_node.name = "print"
            function_node.args = [AstNode(AstNodeType.ARGUMENT)]
            function_node.args[0].value = AstNode.make_node(json_d["expr"])
            node = function_node
        elif node._type == AstNodeType.STATEMENT_WHILE:
            # simple process to discover implicit flows
            var_node = AstNode(AstNodeType.EXPRESSION_VARIABLE)
            var_node.name = f"__anon__{AstNode.__anonymous_var_counter}"
            AstNode.__anonymous_var_counter += 1
            expr_assign = AstNode(AstNodeType.EXPRESSION_ASSIGN)
            expr_assign.var = var_node
            expr_assign.expr = AstNode.make_node(json_d["cond"])
            node.condition = expr_assign
            node.statements = [
                AstNode.make_node(node) for node in json_d["stmts"]
            ]
        elif node._type == AstNodeType.STATEMENT_ELSE:
            node.statements = [
                AstNode.make_node(node) for node in json_d["stmts"]
            ]
        elif node._type == AstNodeType.STATEMENT_BREAK or node._type == AstNodeType.STATEMENT_CONTINUE:
            pass
        elif node._type == AstNodeType.EXPRESSION_PRE_INC or node._type == AstNodeType.EXPRESSION_POST_INC:
            node.var = AstNode.make_node(json_d["var"])
        elif node._type == AstNodeType.EXPRESSION_CONST_FETCH:
            # maybe turn this into a scalar
            node._type = AstNodeType.SCALAR
            node.name = '.'.join(json_d["name"]["parts"])
        elif node._type == AstNodeType.EXPRESSION_BITWISE_NOT:
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.EXPRESSION_BOOLEAN_NOT:
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.EXPRESSION_ARRAY_DIM_FETCH:
            node._type = AstNodeType.EXPRESSION_VARIABLE
            node.name = '$' + json_d["var"]["name"]
        elif node._type == AstNodeType.EXPRESSION_ASSIGN_OP:
            node._type = AstNodeType.EXPRESSION_ASSIGN
            node.var = AstNode.make_node(json_d["var"])
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.EXPRESSION_UNARY:
            node.expr = AstNode.make_node(json_d["expr"])
        elif node._type == AstNodeType.STATEMENT_NOP:
            pass
        else:
            raise ValueError(f"Type not Implemented {node._type}")
        return node

    def __init__(self, _type: AstNodeType):
        self._type = _type
        self.name: str | None = None
        self.value: AstNode | str | None = None
        self.statements: list[AstNode] | None = None
        self.expr: AstNode | None = None
        self.var: AstNode | None = None
        self.args: list[AstNode] | None = None
        self.left: AstNode | None = None
        self.right: AstNode | None = None
        self.elseifs: list[AstNode] | None = None
        self.else_: AstNode | None = None
        self.condition: AstNode | None = None
        self.taint_type = None

    def is_type(self, _type: AstNodeType):
        return self._type == _type

    def accept(self, visitor):
        return visitor.visit(self)
