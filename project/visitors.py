# from enum import Enum
from typing import Dict, List, Set, Optional
from functools import reduce
from php_ast import AstNode, AstNodeType
from copy import deepcopy

# What needs to be done:
#   - Add Sanitization
#         - Dictionary similar to state <node> : [<source of sanitization>]
#   - Fix local TODOS
#   - Add Loops
#   - Non initialized variables are sources of taintage
# statements pegam na lista de grafos e limpam
# expressions sao visitadas so com um estado
# statements calculam novos estados

is_break = False
is_continue = False

class State:
    def __init__(self, state: Dict[str, Set[str]]):
        self.state = state
    
    def __hash__(self):
        s = set()
        for k, v in self.state.items():
            s.add((k, frozenset(v)))

        return hash(frozenset(s))


class Visitor:

    def visit(self, node: AstNode):
        raise NotImplementedError()


class TypeChecker(Visitor):

    @staticmethod
    def is_anonymous(var_name):
        return "__anon__" in var_name

    @staticmethod
    def is_variable(var_name):
        return var_name[0] == '$'

    def __init__(self, max_cycle_depth: int):
        self.depth: int = max_cycle_depth
        self.__scalar_count = 0
        self.states = None

    def visit(self, node: AstNode):
        states = [dict()]
        if node.is_type(AstNodeType.PROGRAM):
            for s in node.statements:
                self.visit_statement(s, states)
        unique_states = dict()
        for state in states:
            key = State(state).__hash__()
            if key not in unique_states:
                unique_states[key] = state
        self.states = [value for (key, value) in unique_states.items()]

    def visit_statement(self,
                        node: AstNode,
                        state: List[Dict],
                        propagated_node: AstNode = None):
        global is_break, is_continue
        new_state = []
        for s in state:
            if node.is_type(AstNodeType.STATEMENT_EXPRESSION):
                new_state += self.visit_expression(node.expr, deepcopy(s),
                                                   propagated_node)
            if node.is_type(AstNodeType.STATEMENT_IF):
                new_state += self.visit_if_statement(node, deepcopy(s),
                                                     propagated_node)
            if node.is_type(AstNodeType.STATEMENT_WHILE):
                new_state += self.visit_while_statement(
                    node, deepcopy(s), propagated_node)
            if node.is_type(AstNodeType.STATEMENT_ECHO):
                pass
            if node.is_type(AstNodeType.STATEMENT_BREAK):
                is_break = True
                new_state.append(deepcopy(s))
            if node.is_type(AstNodeType.STATEMENT_CONTINUE):
                is_continue = True
                new_state.append(deepcopy(s))
            if node.is_type(AstNodeType.STATEMENT_NOP):
                pass
        state.clear()
        state.extend(new_state)
        return new_state

    def visit_expression(self,
                         node: AstNode,
                         state: Dict,
                         propagated_node: AstNode = None,
                         is_condition=False):
        # in expressions there is always the possibility of being in the right side of an assignment
        # so we need to propagate the left side variable so the graph can be built
        if node.is_type(AstNodeType.EXPRESSION_ASSIGN):
            self.visit_expression_assign(node, state, propagated_node,
                                         is_condition)
        if node.is_type(AstNodeType.EXPRESSION_VARIABLE):
            self.visit_expression_variable(node, state, propagated_node,
                                           is_condition)
        if node.is_type(AstNodeType.EXPRESSION_FUNCTION_CALL):
            self.visit_expression_function_call(node, state, propagated_node,
                                                is_condition)
        if node.is_type(AstNodeType.EXPRESSION_BINARY):
            self.visit_expression_binary(node, state, propagated_node,
                                         is_condition)

        if node.is_type(AstNodeType.EXPRESSION_BITWISE_NOT) or node.is_type(AstNodeType.EXPRESSION_BOOLEAN_NOT):
            self.visit_expression(node, state, propagated_node,
                                        is_condition)
        if node.is_type(AstNodeType.SCALAR):
            self.visit_scalar(node, state, propagated_node, is_condition)
        if node.is_type(AstNodeType.EXPRESSION_UNARY):
            self.visit_expression(node.expr, state, propagated_node, is_condition)
        if node._type in (
                AstNodeType.EXPRESSION_PRE_INC,
                AstNodeType.EXPRESSION_POST_INC,
        ):
            self.visit_expression_variable(node.var, state, propagated_node, is_condition)
        return [state]

    def visit_expression_assign(self, node: AstNode, state: Dict,
                                propagated_node: AstNode, is_condition):
        self.visit_expression(
            node.expr, state, node.var, is_condition
        )  # here we propagate the variable so we can build the flow graph
        if propagated_node is not None:  # it means we are not on the right side of an assignment
            if TypeChecker.is_anonymous(
                    propagated_node.name) and not is_condition:
                edges = state.get(node.var.name, set())
                edges.add(propagated_node.name)
                state[node.var.name] = edges
            else:
                edges = state.get(propagated_node.name, set())
                edges.add(node.var.name)
                state[propagated_node.name] = edges
                if TypeChecker.is_variable(
                        node.var.name) and node.var.name not in state:
                    state[node.name] = set(("__UNINITIALIZED__", ))

    def visit_expression_variable(self, node: AstNode, state: Dict,
                                  propagated_node: AstNode,
                                  is_condition) -> Optional[AstNode]:
        if propagated_node is not None:  # it means we are not on the right side of an assignment
            if TypeChecker.is_anonymous(
                    propagated_node.name) and not is_condition:
                edges = state.get(node.name, set())
                edges.add(propagated_node.name)
                state[node.name] = edges
            else:
                edges = state.get(propagated_node.name, set())
                edges.add(node.name)
                state[propagated_node.name] = edges
                if TypeChecker.is_variable(
                        node.name) and node.name not in state:
                    state[node.name] = set(("__UNINITIALIZED__", ))

    def visit_expression_function_call(self, node: AstNode, state: Dict,
                                       propagated_node: AstNode,
                                       is_condition) -> Optional[AstNode]:
        if propagated_node is not None:  # it means we are not on the right side of an assignment
            if TypeChecker.is_anonymous(
                    propagated_node.name) and not is_condition:
                edges = state.get(node.name, set())
                edges.add(propagated_node.name)
                state[node.name] = edges
            else:
                edges = state.get(propagated_node.name, set())
                edges.add(node.name)
                state[propagated_node.name] = edges
                if TypeChecker.is_variable(
                        node.name) and node.name not in state:
                    state[node.name] = set(("__UNINITIALIZED__", ))
        for arg in node.args:
            self.visit_expression(arg.value, state, node)

    def visit_scalar(self, node: AstNode, state: Dict,
                     propagated_node: AstNode,
                     is_condition) -> Optional[AstNode]:
        # name = f"__SCALAR__{self.__scalar_count}"
        name = "__SCALAR__"
        self.__scalar_count += 1
        if propagated_node is not None:  # it means we are not on the right side of an assignment
            if TypeChecker.is_anonymous(propagated_node.name):
                pass
            else:
                edges = state.get(propagated_node.name, set())
                edges.add(name)
                state[propagated_node.name] = edges
                # if TypeChecker.is_variable(node.name) and node.name not in state:
                #     state[node.name] = set(("__UNINITIALIZED__",))

    def visit_expression_binary(self, node: AstNode, state: Dict,
                                propagated_node: AstNode,
                                is_condition) -> Optional[AstNode]:
        self.visit_expression(node.left, state, propagated_node, is_condition)
        self.visit_expression(node.right, state, propagated_node, is_condition)

    def visit_if_statement(self, node: AstNode, state: Dict,
                           propagated_node: AstNode) -> Optional[AstNode]:
        self.visit_expression(node.condition,
                              state,
                              propagated_node,
                              is_condition=True)
        new_states = []

        cond_var = node.condition.var

        enter_state = [deepcopy(state)]
        no_else_no_enter_state = [deepcopy(state)]
        no_enter_state = [deepcopy(state)]
        # elseif_states = [[deepcopy(state)] for _ in range(len(node.elseifs))]
        # might provide repeated states, need hashing to make a set
        for s in node.statements:
            new_state = self.visit_statement(s, enter_state, cond_var)
            enter_state = new_state
        if len(node.statements) > 0:
            new_states += enter_state
        # for i, s in enumerate(node.elseifs):
        #     new_state = self.visit_statement(s, elseif_states[i], cond_var)
        #     elseif_states[i] = new_state
        # if len(node.elseifs) > 0:
        #     new_states += reduce(lambda x, y: x + y, elseif_states, [])
        for s in node.else_.statements if node.else_ else []:
            new_state = self.visit_statement(s, no_enter_state, cond_var)
            no_enter_state = new_state
        if len(node.else_.statements if node.else_ else []) > 0:
            new_states += no_enter_state
        else:
            new_states += no_else_no_enter_state

        return new_states

    def visit_while_statement(self, node: AstNode, state: Dict,
                              propagated_node: AstNode):
        global is_continue, is_break
        self.visit_expression(node.condition,
                              state,
                              propagated_node,
                              is_condition=True)
        new_states = []
        cond_var = node.condition.var
        initial_state = [[deepcopy(state)] for _ in range(self.depth)]
        for iteration in range(self.depth):
            for s in node.statements:
                new_state = self.visit_statement(s, initial_state[iteration],
                                                 cond_var)
                initial_state[iteration] = new_state
                if is_continue:
                    is_continue = False
                    break
                if is_break:
                    break
            if is_break:
                is_break = False
                initial_state = initial_state[:iteration + 1]
                break
            if iteration != self.depth - 1:
                initial_state[iteration + 1] = deepcopy(
                    initial_state[iteration])
        return reduce(lambda x, y: x + y, initial_state, [deepcopy(state)])