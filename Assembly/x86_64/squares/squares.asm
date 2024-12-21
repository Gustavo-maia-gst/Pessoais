section .data
    maxNum dw 10
    resSum dw 0
    eqText db "Correct Answer!", 10
    neqText db "Incorrect Answer!", 10

section .text
    global _start

_start:
    mov rcx, 0
    call _sumLoop

    mov ax, word [resSum]
    cmp ax, 385
    je _isEqual
    jmp _notEqual

_sumLoop:
    inc rcx
    mov rax, rcx
    mul rax
    add word [resSum], ax

    cmp cx, word [maxNum]
    jne _sumLoop

_isEqual:
    mov rax, 1
    mov rdi, 1
    mov rsi, eqText
    mov rdx, 16
    syscall
    call _exit

_notEqual:
    mov rax, 1
    mov rdi, 1
    mov rsi, neqText
    mov rdx, 18
    syscall
    call _exit

_exit:
    mov rax, 60
    mov rdi, 0
    syscall
