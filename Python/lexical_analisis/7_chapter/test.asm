section .bss
        a resb 1
        i resb 1
        b resb 1
        c resb 1
        result resb 1
section .text
        global _start
_start:
        mov rax, 0
        mov [i], al
        mov rax, 0
        mov [a], al
        mov rax, 1
        mov [b], al

l001:
        movzx rax, byte [i]
        push rax
        mov rax, 4
        pop rbx
        cmp rax, rbx
        setge al
        movzx rax, al
        cmp rax, 0
        je l002
        movzx rax, byte [a]
        push rax
        movzx rax, byte [b]
        pop rbx
        add rax, rbx
        mov [c], al
        movzx rax, byte [b]
        mov [a], al
        movzx rax, byte [c]
        mov [b], al
        movzx rax, byte [i]
        push rax
        mov rax, 1
        pop rbx
        add rax, rbx
        mov [i], al
        jmp l001

l002:
        movzx rax, byte [b]
        mov [a], al
        call _print
        call _exit

_print:
        add rax, 0x30
        mov byte [result], al
        mov rax, 1
        mov rdi, 1
        mov rsi, result
        mov rdx, 1
        syscall
        mov byte [result], 10
        mov rax, 1
        mov rdi, 1
        mov rsi, result
        mov rdx, 1
        syscall
        ret

_exit:
        mov rax, 60
        mov rdi, 0
        syscall
