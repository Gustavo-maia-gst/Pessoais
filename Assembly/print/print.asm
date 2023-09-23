section .data
	num dd 3515
	numLen db 4

section .bss
	numString resb 4

section .text
	global _start

_start:
	mov eax, dword [num]
	mov bl, byte [numLen]
	push rbx
	push rax

_intToStr:
	pop rax
	pop rbx
	mov ecx, 10
	xor rdx, rdx

_intToStrLoop:
	div rcx
	push rdx
	xor rdx, rdx
	cmp rax, 0
	jne _intToStrLoop
	xor rcx, rcx

_stackToStrLoop:
	pop rax
	add rax, 0x30
	mov byte [numString + rcx], al
	inc rcx
	cmp rcx, rbx
	jne _stackToStrLoop
	mov byte [numString + rcx], 10

_printInteger:
	mov rax, 1
	mov rdi, 1
	mov rsi, numString
	mov dl, byte [numLen]
	inc dl
	syscall

_exit:
	mov rax, 60
	mov rdi, 0
	syscall
