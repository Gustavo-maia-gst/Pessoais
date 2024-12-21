section .data
	fibNum db 20
	finRes dd 0

section .text
	global _start

_start:
	mov eax, 1
	mov ebx, 0
	mov edx, 0
	mov rcx, byte [fibNum]

	call _fibLoop

	mov dword [finRes], ebx

	mov rax, 60
	mov rdi, 0
	syscall

_fibLoop:
	mov edx, ebx
	mov ebx, eax
	add eax, edx

	dec rcx
	cmp rcx, 0
	ja _fibLoop
	ret

