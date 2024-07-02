.data

endl: .asciiz "\n"
x: .word	0:1

.text

main:
sw $fp 0($sp)
addiu $sp $sp-4
jal suma
sw $a0 x
lw $a0 x
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 1
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
li $v0 1
syscall
li $v0 4
la $a0 endl
syscall
li $v0 10
syscall
suma:
move $fp $sp
sw $ra 0($sp)
addiu $sp $sp -4
li $a0 1
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 2
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
lw $ra 4($sp)
addiu $sp $sp 8
lw $fp 0($sp)
jr $ra