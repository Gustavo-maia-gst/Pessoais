section .data
	number dd 441

section .bss
	sqrt dd 1

section .text
	global _start

_start:
	mov rbx, 123					; The value of the rbx should not be changed.

	mov edi, dword [number] 		; 1st parameter of the function.
	call _sqrt
	mov dword [sqrt], eax

	mov rax, 60
	mov rdi, 0
	syscall

_sqrt:
	push rbx 						; This line pushes the value of to the stack, this value should be setted back to rbx.
	mov ebx, edi
	mov rcx, 50
	
	call _sqrtLoop
	mov eax, ebx
	pop rbx
	ret

_sqrtLoop:
	mov eax, edi
	xor rdx, rdx
	div ebx
	add eax, ebx
	shr eax, 1
	mov esi, ebx
	mov ebx, eax

	cmp ebx, esi
	je _sqrtFinded

	dec rcx
	cmp rcx, 0
	jne _sqrtLoop

	ret
	
_sqrtFinded:
	ret
