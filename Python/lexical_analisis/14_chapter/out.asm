section .bss
	result resq 1

section .text
	global _start

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

l001:
	push rbp
	mov rbp, rsp
	mov rax, [rbp + 24]
	push rax
	mov rax, [rbp + 16]
	pop rbx
	cmp rax, rbx
	sete al
	movzx rax, al
	cmp rax, 0
	je l002
	add rsp, 0
	mov rsp, rbp
	pop rbp
	ret
	
l002:
	mov rax, [rbp + 24]
	sub rsp, 8
	mov [rbp - 8], rax
	call _print
	add rsp, 0
	mov rax, [rbp + 24]
	push rax
	mov rax, 1
	pop rbx
	add rax, rbx
	push rax
	mov rax, [rbp + 16]
	push rax
	call l001
	add rsp, 16
	add rsp, 8
	mov rsp, rbp
	pop rbp
	ret
	add rsp, 8
	mov rsp, rbp
	pop rbp
	ret

_start:
	push rbp
	mov rbp, rsp
	mov rax, 2
	push rax
	mov rax, 7
	push rax
	call l001
	add rsp, 16
	call _exit


