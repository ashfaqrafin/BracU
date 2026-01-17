#!/bin/bash

set -e

# Always run from this script's directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

bison -d -y --debug --verbose syntax_analyzer.y
echo 'Generated the parser C file as well the header file'
g++ -w -c -o y.o y.tab.c
echo 'Generated the parser object file'
flex lex_analyzer.l
echo 'Generated the scanner C file'
g++ -fpermissive -w -c -o l.o lex.yy.c
echo 'Generated the scanner object file'
g++ y.o l.o -o parser.out
echo 'All ready, running'

mkdir -p InputOutput
for i in 1 2 3; do
    if [ -f "InputOutput/input${i}.c" ]; then
        ./parser.out "InputOutput/input${i}.c"
        cp -f log.txt "InputOutput/log${i}.txt"
        echo "==== Input ${i} -> Output saved to InputOutput/log${i}.txt ===="
    fi
done

echo 'Done.'
