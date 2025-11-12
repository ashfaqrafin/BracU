#!/bin/bash

# Generate parser
bison -d -y --debug --verbose syntax_analyzer.y
echo 'Generated the parser C file as well the header file'

# Compile parser
g++ -w -c -o y.o y.tab.c
echo 'Generated the parser object file'

# Generate lexer
flex lex_analyzer.l
echo 'Generated the scanner C file'

# Compile lexer
g++ -fpermissive -w -c -o l.o lex.yy.c
echo 'Generated the scanner object file'

# Link and create executable
g++ y.o l.o -o a.out
echo 'All ready, running'

# Run the program
./a.out input.txt