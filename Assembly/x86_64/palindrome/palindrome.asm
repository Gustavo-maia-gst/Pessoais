section .data
	num db 35, 32, 30, 45, 30, 32, 35, 00
	sentinel db 00

section .bss
	numLen db 1
	palindrome db 1
	result resb 1

section .text
	global _start

_start:
	call _getNumLen
	mov byte [numLen], cl

_isPalindrome:
	xor rax, rax
	mov al, byte [numLen]
	shr rax, 1
	xor rbx, rbx
	xor rcx, rcx
	xor rdx, rdx
	xor rdi, rdi
	mov cl, byte [numLen]
	dec cl

_isPalindromeLoop:
	mov dil, byte [num + rdx]
	mov sil, byte [num + rcx]
	dec rcx
	inc rdx
	cmp dil, sil
	jne _isNot
	cmp cl, al
	jne _isPalindromeLoop
	jmp _is

_isNot:
	mov byte [result], 0
	jmp _exit

_is:
	mov byte [result], 1
	jmp _exit

_exit:
	mov rax, 60
	mov rdi, 0
	syscall

_getNumLen:
     mov rbx, 0
     mov rcx, 0
     mov rax, num
 
_getNumLenLoop:
     mov bl, byte [rax + rcx]
     inc rcx
     cmp bl, byte [sentinel]
     jne _getNumLenLoop
     dec rcx
     ret	
