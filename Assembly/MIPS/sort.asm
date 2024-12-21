_start:
    addi $s0, $zero, 1
sort:
    slt $t0, $s0, $a1
    beq $t0, $zero, endSort

    addi $s1, $s0, -1
inner:
    slt $t0, $s1, $zero
    bne $t0, $zero, endInner
    sll $t0, $s1, 2
    add $t1, $t0, $a0
    lw $t2, 0($t1)
    lw $t3, 4($t1)
    slt $t0, $t3, $t2
    beq $t0, $zero, endInner
    sw $t3, 0($t1)
    sw $t2, 4($t1)
    j inner
endInner:
    addi $s0, $s0, 1
    j sort
endSort:
    end
    
