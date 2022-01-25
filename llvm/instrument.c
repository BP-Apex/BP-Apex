#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <assert.h>
static FILE* fpexec = NULL;
static FILE* fpargs = NULL;
static FILE* fpvars = NULL;
static FILE* fpinput = NULL;
static int args = 0;
static int argc;
static char** argv;
static void* memory = NULL;

void __instrument1(long id, unsigned long value) {
  if (!fpexec) fpexec = fopen("exec.out", "w");
  fprintf(fpexec, "(I %ld %ld 1)\n", id, value);
  fflush(fpexec);
}

void __instrument2(long id, unsigned long value) {
  if (!fpexec) fpexec = fopen("exec.out", "w");
  fprintf(fpexec, "(I %ld %ld 2)\n", id, value);
  fflush(fpexec);
}

void __main_args(void* ptr) {
  if (!fpargs) fpargs = fopen("args.out", "w");
  // fprintf(fpargs, "(args %d %ld)\n", args, ptr);
  // fflush(fpargs);
  if (args == 0)
    argc = (int)ptr;
  else {
    argv = (char**)ptr;
    for(int i = 1; i < argc; i++) {
      char* p = argv[i];
      do {
        fprintf(fpargs, "%lx %d\n", (unsigned long)p, *p);
      } while(*(p++));
      fprintf(fpargs, "\n");
    }
  }
  fflush(fpargs);

  args++;
}

void INPUT_CHAR_ARRAY(int* var) {
  if (!fpargs) fpargs = fopen("args.out", "w");
  if (!fpinput) fpinput = fopen("input", "r");

  char c;

  do {
    *(var) = c = fgetc(fpinput);
    fprintf(fpargs, "%lx %d\n", (unsigned long)var, *var);
    fflush(fpargs);
    ++var;
  } while (c != EOF);
  *(var) = EOF;

  // *var = fgetc(fpinput);
  //fscanf(fpinput, "%c", var);
}

void INPUT_VARIABLE(int* var) {
  if (!fpargs) fpargs = fopen("args.out", "w");
  if (!fpinput) fpinput = fopen("input", "r");

  fscanf(fpinput, "%d", var);
  fprintf(fpargs, "%lx %d\n", (unsigned long)var, *var);
  fflush(fpargs);
}

void INPUT_ARRAY(int* array, int len, int n) {
  if (!fpargs) fpargs = fopen("args.out", "w");
  if (!fpinput) fpinput = fopen("input", "r");
  for (int i = 0; i < n; i++) {
    int *v = &array[i];
    fscanf(fpinput, "%d", v);
    fprintf(fpargs, "%lx %d\n", (unsigned long)v, *v);
    fflush(fpargs);
  }
}

void INPUT_MATRIX(int* matrix, int row, int col, int m, int n) {
  if (!fpargs) fpargs = fopen("args.out", "w");
  if (!fpinput) fpinput = fopen("input", "r");
  for (int r = 0; r < m; r++) {
    for (int c = 0; c < n; c++) {
      int *v = &matrix[r * col + c];
      fscanf(fpinput, "%d", v);
      fprintf(fpargs, "%lx %d\n", (unsigned long)v, *v);
      fflush(fpargs);
    }
  }
  fflush(fpargs);
}
/*
void* __my_malloc(int size) {
  if (!memory) {
    memory = mmap((void*)0xa0000000, 0x10000000, PROT_READ | PROT_WRITE,
        MAP_PRIVATE | MAP_FIXED | MAP_ANON, -1, 0);
    assert (memory != MAP_FAILED);
  }
  void* addr = memory;
  memory += size;
  return addr;
}

void INTERNAL_ARRAY(void** array, int len) {
  if (!fpvars) fpvars = fopen("vars.out", "w");

  *array = __my_malloc(len);
  fprintf(fpvars, "%lx %ld\n", (unsigned long)array, (unsigned long)*array);
  fflush(fpvars);
}
*/
void INTERNAL_VARIABLE(int* var) {
  if (!fpvars) fpvars = fopen("vars.out", "w");

  fprintf(fpvars, "%lx %d\n", (unsigned long)var, *var);
  fflush(fpvars);
}

int pow(int x, int n) {
  int r = 1;
  for (int i = 0; i < n; i++)
    r *= x;
  return r;
}

void DESCRIPTION(const char* str) { }
void END_DESCRIPTION() { }
