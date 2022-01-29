BPEX := $(shell dirname "$(shell pwd)")
CFLAGS=-g -O0 -include ${BPEX}/llvm/common.h -Wall -Werror=implicit-function-declaration -fno-builtin -std=c99 -Wno-unused-variable -Wno-unused-value -DNDEBUG
CLANG=clang-3.7
OPT=${BPEX}/llvm/opt -load ${BPEX}/llvm/LLVMHello.so
LLC=${BPEX}/llvm/llc
LD=gcc
CC=gcc

.PHONY: all clean run build

all: build run
run: symb.out
build: exec cfg.out
clean:
	rm -f exec *.xxx src.*.o *.bc *.out stdout *.log *.bc.*

src.1.bc: src.c
	${CLANG} -c -emit-llvm ${CFLAGS} $< -o $@

exec: src.3.o ${BPEX}/llvm/instrument.o
	${LD} -o $@ $^ -lm

src.2.bc: src.1.bc
	${OPT} -constantexpr $< -o $@

src.3.bc: src.2.bc
	${OPT} -mystuff $< -o $@

cfg.out: src.3.bc
	${BPEX}/scripts/llvm_cfg.py

exec.out: exec input
	./exec < input > stdout

symb.out: exec exec.out cfg.out
	${BPEX}/scripts/symbexec.py -out symb.out -cfg cfg.out -llvm llvm.out -exec exec.out -args args.out

${BPEX}/llvm/instrument.o: ${BPEX}/llvm/instrument.c
	${CC} -g -O0 -std=c99 -c -o $@ $<

%.s: %.bc
	${LLC} -O0 $< -o $@
%.o: %.s
	${CC} -c $<

.DELETE_ON_ERROR:
