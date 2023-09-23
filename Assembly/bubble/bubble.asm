section .data
	sentinel db 0xFF
	array db 4, 7, 1, 3, 12, 5, 0, 8, 0xFF

section .bss
	arrayLen resb 1

section .text
	global _start

_start:
	call _getArrayLen
	mov byte [arrayLen], al

	mov rsi, array
	mov al, byte [arrayLen]
	dec rax
	xor rbx, rbx
	xor rcx, rcx
	xor rdx, rdx

	mov bl, byte [arrayLen]
	call _bubbleSort

	mov rax, 60
	mov rdi, 0
	syscall

_getArrayLen:
	mov bl, 0xFF
	xor rax, rax
	xor rcx, rcx
	
	mov rsi, array
	call _getArrayLenLoop
	dec rax
	ret

_getArrayLenLoop:
	mov cl, byte [rsi + rax]
	inc rax
	cmp cl, bl
	jne _getArrayLenLoop
	ret

_bubbleSort:
	mov cl, byte [rsi + rax]
	mov r8b, al
	dec r8b
	call _secLoop
	dec rax
	cmp al, 0
	mov dl, 0
	jne _bubbleSort
	ret

_swap:
	mov	byte [rsi + rdx], dil
	mov byte [rsi + rdx - 1], r9b

_secLoop:
	mov dil, byte [rsi + rdx]
	mov r9b, byte [rsi + rdx + 1]
	inc dl
	cmp dil, r9b
	ja _swap
	cmp dl, r8b
	jb _secLoop
	ret

