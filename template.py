from parser import NodeType

TMPL_PTR_INC = """
    add rcx, {val}
"""

TMPL_PTR_DEC = """
    sub rcx, {val}
"""

TMPL_INC = """
    mov al, [rbp - {mem_size} + rcx]
    add al, {val}
    mov [rbp - {mem_size} + rcx], al
"""

TMPL_DEC = """
    mov al, [rbp - {mem_size} + rcx]
    sub al, {val}
    mov [rbp - {mem_size} + rcx], al
"""

TMPL_INPUT = """
    lea rdi, [rbp - {mem_size} + rcx]
    push rcx
    call read
    pop rcx
"""

TMPL_OUTPUT = """
    lea rdi, [rbp - {mem_size} + rcx]
    push rcx
    call write
    pop rcx
"""

TMPL_START_BRACKET = """
start_bracket_{val}:
    mov al, [rbp - {mem_size} + rcx]
    test al, al
    jz end_bracket_{val}
"""

TMPL_END_BRACKET = """
    jmp start_bracket_{val}
end_bracket_{val}:
"""

TEMPLATES = {
    NodeType.PTR_INC: TMPL_PTR_INC,
    NodeType.PTR_DEC: TMPL_PTR_DEC,
    NodeType.INC: TMPL_INC,
    NodeType.DEC: TMPL_DEC,
    NodeType.INPUT: TMPL_INPUT,
    NodeType.OUTPUT: TMPL_OUTPUT,
    NodeType.START_BRACKET: TMPL_START_BRACKET,
    NodeType.END_BRACKET: TMPL_END_BRACKET
}

ASM_TEMPLATE = """
_start:
    mov rbp, rsp
    sub rsp, {0}
    mov rcx, {1}
    {2}
    mov rdi, 0
    mov rax, 60
    syscall
    ret

read:
    mov rsi, rdi
    mov rdi, 0
    mov rax, 0
    mov rdx, 1
    syscall
    ret

write:
    mov rsi, rdi
    mov rdi, 1
    mov rax, 1
    mov rdx, 1
    syscall
    ret
"""
