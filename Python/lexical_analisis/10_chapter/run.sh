python3 assembler.py $1 > out.asm 2>> out.asm

if [ $? != 0 ]; then
    echo "Error generating the code:"
    cat out.asm
    rm out.asm
    exit 1
fi

yasm -f elf64 -o out.o out.asm 2> .log.txt
ld -o out out.o 2> /dev/null

if [ $? != 0 ]; then
    echo "Error compiling the code:"
    cat log.txt
    rm .log.txt
    exit 1
fi

if [ $? = 0 ]; then
    echo -e "Generated source code:\n"
    cat out.asm
    echo "Result: "
    rm out.o .log.txt
    ./out
    rm out out.asm
fi
