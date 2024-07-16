python3 assemblerv2.py $1 > out.asm 2> /dev/null
yasm -f elf64 -o out.o out.asm 2> /dev/null
ld -o out out.o 2> /dev/null
if [ $? = 0 ]; then
    echo -e "Generated source code:\n"
    cat out.asm
    echo "Result: "
    ./out
        rm out out.o out.asm
fi
