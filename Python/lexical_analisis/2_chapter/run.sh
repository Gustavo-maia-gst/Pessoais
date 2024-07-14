python3 main.py > out.asm
yasm -f elf64 -o out.o out.asm 2> /dev/null
ld -o out out.o 2> /dev/null
if [ -f out ]; then
    echo -e "Generated source code:\n"
    cat out.asm
    rm out.asm out.o
    echo "Result: "
    ./out
    rm out
fi
