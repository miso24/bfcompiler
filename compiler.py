from parser import Parser, NodeType
from keystone import *
from template import TEMPLATES, ASM_TEMPLATE

class Compiler:
    def __init__(self, mem_size=100):
        self.mem_size = mem_size

    def compile(self, code):
        parser = Parser(code)
        parser.parse()

        asm = ""
        for node in parser.nodes:
            node_type = node.node_type
            if node_type in [NodeType.PTR_INC, NodeType.PTR_DEC, NodeType.END_BRACKET]:
                asm += TEMPLATES[node_type].format(val=node.val)
            elif node_type in [NodeType.INPUT, NodeType.OUTPUT]:
                asm += TEMPLATES[node_type].format(mem_size=self.mem_size)
            elif node_type in [NodeType.INC, NodeType.DEC, NodeType.START_BRACKET]:
                asm += TEMPLATES[node_type].format(mem_size=self.mem_size, val=node.val)
        asm_code = ASM_TEMPLATE.format(self.mem_size,self.mem_size // 2, asm)
        ks = Ks(KS_ARCH_X86, KS_MODE_64)
        encoding, _ = ks.asm(asm_code)
        return bytes(encoding)
