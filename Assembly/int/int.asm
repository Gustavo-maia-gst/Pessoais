section .data
	string db 0x32, 0x30, 0x30, 0x35

section .bss
	num resw 1

section .text
	global _start

_start:
	mov rdi, string
	mov rsi, 4

	call _strToInt
	mov word [num], ax
	
	mov rax, 60
	mov rsi, 0
	syscall

_strToInt:
	mov rcx, 1
	xor rax, rax
	xor rdx, rdx

_strToIntLoop:
	xor r10, r10
	xor r11, r11

	mov r10, rsi
	sub r10, rcx

	push rax
	push rdi
	push rsi

	mov rdi, 10
	mov rsi, r10
	call _power
	mov r10, rax
	
	pop rsi
	pop rdi
	
	mov r11b, byte [rdi + rcx - 1]
	sub r11, 0x30
	mov rax, r11
	mul r10
	mov r11, rax
	pop rax
	add rax, r11

	inc rcx
	cmp rcx, rsi
	jbe _strToIntLoop

	ret

_power:
	mov rax, 1
	cmp rsi, 0
	jne _powerLoop
	mov rax, 1
	ret

_powerLoop:
	mul rdi

	dec rsi
	cmp rsi, 0
	jne _powerLoop
	ret
