from abc import ABCMeta
from enum import Enum

class Node():
    def __init__(self, node_type, val=0):
        self.node_type = node_type
        self.val = val 

class BracketNode(Node):
    def __init__(self, node_type):
        self.node_type = node_type

class NodeType(Enum):
    PTR_INC = 0
    PTR_DEC = 1
    INC = 2
    DEC = 3
    OUTPUT = 4
    INPUT = 5
    START_BRACKET = 6
    END_BRACKET = 7

class BrainfuckSyntaxError(Exception):
    pass

class Parser:
    def __init__(self, code):
        self.nodes = []
        self.bracket_stack = []
        self.code = code
        self.ip = 0
        self.bracket_id = 0

    def parse_repeat_node(self, node_type, node_char):
        repeat = 1
        self.ip += 1
        while not self.is_eoc() and self.code[self.ip] == node_char:
            repeat += 1
            self.ip += 1
        self.nodes.append(Node(node_type, val=repeat))

    def parse(self):
        while not self.is_eoc():
            if self.code[self.ip] == "+":
                self.parse_repeat_node(NodeType.INC, "+")
                continue
            elif self.code[self.ip] == "-":
                self.parse_repeat_node(NodeType.DEC, "-")
                continue
            if self.code[self.ip] == "<":
                self.parse_repeat_node(NodeType.PTR_DEC, "<")
                continue
            elif self.code[self.ip] == ">":
                self.parse_repeat_node(NodeType.PTR_INC, ">")
                continue
            elif self.code[self.ip] == ".":
                self.nodes.append(Node(NodeType.OUTPUT))
            elif self.code[self.ip] == ",":
                self.nodes.append(Node(NodeType.INPUT))
            elif self.code[self.ip] == "[":
                self.bracket_stack.append(self.bracket_id)
                self.nodes.append(Node(NodeType.START_BRACKET, val=self.bracket_id))
                self.bracket_id += 1
            elif self.code[self.ip] == "]":
                try:
                    self.nodes.append(Node(NodeType.END_BRACKET, self.bracket_stack.pop()))
                except IndexError:
                    raise BrainfuckSyntaxError("Illegal number of brackets")
            self.ip += 1
        if self.bracket_stack:
            raise BrainfuckSyntaxError("Illegal number of brackets")

    def is_eoc(self):
        return self.ip >= len(self.code)
