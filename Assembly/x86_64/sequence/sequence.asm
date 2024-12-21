section .data
	nums dw 21, 5, 63, 31, 45, 10, 0
	sentinel dw 0

section .bss
	maxNum resw 1
	minNum resw 1
	middleNum resw 1
	numsLen resb 1
	numsSum resw 1

section .text
	global _start

_start:
	call _getNumsLen
	mov byte [numsLen], cl

	call _sumNums
	mov word [numsSum], ax

	call _minNums
	mov word [minNum], ax
	
	call _maxNums
	mov word [maxNum], ax

	call _middleNums
	mov word [middleNum], ax

	mov rax, 60
	mov rdi, 0
	syscall

_minNums:
	mov ax, word [nums]
	xor rbx, rbx
	mov sil, byte [numsLen]
	dec rsi
	mov rdx, nums
	xor rcx, rcx
	call _minNumsLoop
	ret

_chmin:
	mov ax, bx
	ret

_minNumsLoop:
	inc rcx
	mov bx, word [rdx + rcx * 2]
	cmp bx, ax
	jb _chmin
	cmp rcx, rsi
	jne _minNumsLoop
	ret

_maxNums:
	mov ax, word [nums]
	xor rbx, rbx
	xor rcx, rcx
	mov rdx, nums
	mov sil, byte [numsLen]
	dec rsi
	call _maxNumsLoop
	ret

_chmax:
	mov ax, bx
	ret

_maxNumsLoop:
	inc rcx
	mov bx, word [rdx + rcx * 2]
	cmp bx, ax
	ja _chmax
	cmp rcx, rsi
	jne _maxNumsLoop
	ret

_sumNums:
	mov ax, 0
	mov bx, 0
	mov rcx, 0
	mov rdx, nums
	mov sil, byte [numsLen]

_sumNumsLoop:
	mov bx, word [rdx + 2 * rcx]
	add ax, bx
	inc rcx
	cmp rcx, rsi
	jne _sumNumsLoop
	ret

_getNumsLen:
	mov rbx, 0
	mov rcx, 0
	mov rax, nums

_getNumsLenLoop:
	mov bx, word [rax + 2 * rcx]
	inc rcx
	cmp bx, word [sentinel]
	jne _getNumsLenLoop
	dec rcx
	ret

_middleNums:
	xor rdx, rdx
	xor rax, rax
	mov al, byte [numsLen]
	mov ebx, 2
	div ebx
	cmp rdx, 0
	je _evenValue
	jmp _oddValue
	ret

_oddValue:
	mov rsi, nums
	mov bx, word [rsi + rax * 2]
	mov rax, rbx
	ret

_evenValue:
	dec rax
	mov rsi, nums
	mov bx, word [rsi + 2 * rax]
	mov cx, word [rsi + 2 * rax + 2]
	add rbx, rcx
	mov rax, rbx
	mov rbx, 2
	div rbx
	ret
