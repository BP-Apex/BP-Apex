#define NULL 0
//#define double int
//#define float int
//#define long int
#define bool int
#define fprintf(fp, ...) printf(__VA_ARGS__)
#define atof(x) atoi(x)
#define cosf(x) cos(x)
#define sinf(x) sin(x)
#define logf(x) log(x)
#define expf(x) exp(x)
#define powf(x, n) pow(x, n)
#define sprint_dec(s, x) sprintf(s, "%d", x)
#define sprint_chr(s, x) sprintf(s, "%c", x)
#define sprint_hex(s, x) sprintf(s, "%x", x)
#define strtod(nptr, endptr) strtol(nptr, endptr, 10)
#define EOF (-1)

typedef unsigned long size_t;

#ifdef __cplusplus
extern "C" {
#endif
  void* malloc(size_t size);
  void* calloc(size_t nmemb, size_t size);
  void* realloc(void *ptr, size_t size);
  void  free(void*);
  void  abort(void);
  void  exit(int);

  int printf (const char *format, ...);
  int sprintf(char* s, const char* fmt, ...);
  int sscanf (const char* str, const char *format, ...);

  int abs(int);
  int pow(int, int);

  int atoi(const char *nptr);
 
  size_t strlen(const char *s);
  char*  strdup(const char *p);
  char*  strcat(char* d, const char* s);
  char*  strcpy(char* d, const char* s);
  char*  strchr(const char* s, int c);
  char*  strrchr(const char* s, int c);
  int    strcmp(const char *s1, const char *s2);
  int    strtol(const char *nptr, char **endptr, int base);
  char*  strncat(char* d, const char* s, size_t n);
 
  void*  memcpy(void *dest, const void *src, size_t n);
  void*  memset(void *dest, int c, size_t n);

  int isalpha(int c);
  int isdigit(int c);
  int isspace(int c);
  int toupper(int c);
  int tolower(int c);

  void INPUT_CHAR_ARRAY(int*);
  void INPUT_VARIABLE(int*);
  void INPUT_MATRIX(int*, int, int, int, int);
  void INTERNAL_VARIABLE(int*);
  void INTERNAL_ARRAY(void**, int);
  void DESCRIPTION(const char*);
  void END_DESCRIPTION();

  double sin(double);
  double cos(double);
  double tan(double);
  double exp(double);
  double log(double);

  int errno;

#define	EINVAL		22	/* Invalid argument */
// #define M_E		2.7182818284590452354	/* e */
// #define M_PI		3.14159265358979323846	/* pi */
// struct FILE;
// typedef struct FILE FILE;
// extern struct FILE* stdout;
// extern struct FILE* stderr;
// 
// int abs(int x) __attribute__((section("mylib")));
// int abs(int x) {
//   if (x < 0)
//     return -x;
//   else
//     return x;
// }
// 
// 
// // int pow(int x, int n) __attribute__((section("mylib")));
// // int pow(int x, int n) {
// //   int r = 1;
// //   int i;
// //   for (i = 0; i < n; i++)
// //     r *= x;
// //   return r;
// // }
// // // float powf(float x, float y) __attribute__((section("mylib"), alias("pow")));
// 
// 
// int __itoa(char *str, int v, int base) __attribute__((section("mylib")));
// int __itoa(char *str, int v, int base) {
//   int i = 0;
//   int j;
//   do {
//     int digit = v % base;
//     v = v / base;
//     if (digit < 10)
//       str[i++] = digit + '0';
//     else
//       str[i++] = digit - 10 + 'A';
//   } while(v);
//   str[i] = '\0';
//   --i;
//   for (j = 0; j < i; ++j,--i) {
//     char t = str[i];
//     str[i] = str[j];
//     str[j] = t;
//   }
//   return 1;
// }
// 
// 
// int sprint_dec(char* str, int x) __attribute__((section("mylib")));
// int sprint_dec(char* str, int x) {
//   __itoa(str, x, 10);
//   return 1;
// }
// 
// int sprint_hex(char* str, int x) __attribute__((section("mylib")));
// int sprint_hex(char* str, int x) {
//   __itoa(str, x, 16);
//   return 1;
// }
// 
// int sprint_chr(char* str, int x) __attribute__((section("mylib")));
// int sprint_chr(char* str, int x) {
//   str[0] = (char)x;
//   str[1] = 0;
//   return 1;
// }
// 
// 
// // int sprintf (char* str, const char* format, ...) __attribute__((section("mylib"), format(printf, 2, 3)));
// // int sprintf (char* str, const char* format, ...) {
// //   va_list ap;
// //   va_start(ap, format);
// // 
// //   if (format[0] != '%' || format[2] != '\0') abort();
// // 
// //   if (format[1] == 'x' || format[1] == 'X') {
// //     __itoa(str, va_arg(ap, int), 16);  
// //   }
// //   else if (format[1] == 'd') {
// //     __itoa(str, va_arg(ap, int), 10);  
// //   }
// //   else if (format[1] == 'c') {
// //     str[0] = va_arg(ap, int);
// //     str[1] = '\0';
// //   }
// //   else {
// //     abort();
// //   }
// // 
// //   va_end(ap);
// //   return 1;
// // }
// 
// 
// int strtol(const char* str, char** endptr, int base) __attribute__((section("mylib")));
// int strtol(const char* str, char** endptr, int base) {
//   int r = 0;
//   int s = 1;
//   const char* oldstr = str;
//   int any = 0;
// 
//   if (*str == '-') {
//     s = -1;
//     ++str;
//   }
//   else if (*str == '+') {
//     s = 1;
//     ++str;
//   }
// 
//   while (*str)  {
//     int digit = 0;
//     if ('0' <= *str && *str <= '9') digit = *str - '0';
//     else if ('a' <= *str && *str <= 'z') digit = *str - 'a' + 10;
//     else if ('A' <= *str && *str <= 'Z') digit = *str - 'A' + 10;
//     else break;
// 
//     if (digit >= base) break;
//     any = 1;
//     r = r * base + digit;
//     ++str;
//   }
// 
//   if (endptr) {
//     if (any) *endptr = (char*)str;
//     else *endptr = (char*)oldstr;
//   }
// 
//   if (str == oldstr) errno = EINVAL;
//   return s*r;
// }
// 
// 
// // int atoi(const char *s) __attribute__((section("mylib")));
// // int atoi(const char *s) {
// //   int r = strtol(s, NULL, 10);
// //   return r;
// // }
// // // int atof (const char *s) __attribute__((section("mylib"), alias("atoi")));
// // // int atoll(const char *s) __attribute__((section("mylib"), alias("atoi")));
// 
// 
// double strtod(const char* str, char** endptr) __attribute__((section("mylib")));
// double strtod(const char* str, char** endptr) {
//   double r = strtol(str, endptr, 10);
//   return r;
// }
// 
// 
// // int strlen(const char* str) __attribute__((section("mylib")));
// // int strlen(const char* str) {
// //   int r = 0;
// //   while (*str) {++str; ++r;}
// //   return r;
// // }
// 
// 
// char* strcpy(char *d, const char *s) __attribute__((section("mylib")));
// char* strcpy(char *d, const char *s) {
//   char *dest = d;
//   for (; *s; ++s,++d) *d = *s;
//   *d = '\0';
//   return dest;
// }
// 
// 
// char* strcat(char *d, const char *s) __attribute__((section("mylib")));
// char* strcat(char *d, const char *s) {
//   char *dest = d;
//   for (; *d; ++d);
//   for (; *s; ++d,++s) *d = *s;
//   *d = '\0';
//   return dest;
// }
// 
// 
// char* strncat(char *d, const char *s, size_t n) __attribute__((section("mylib")));
// char* strncat(char *d, const char *s, size_t n) {
//   char *dest = d;
//   for (; *d; ++d);
//   for (; ; ++d,++s,--n) {
//     if (!(*s && n)) break;
//     *d = *s;
//   }
//   *d = '\0';
//   return dest;
// }
// 
// 
// char* strdup(const char *s) __attribute__((section("mylib")));
// char* strdup(const char *s) {
//   char* p = (char*)malloc(30);
//   strcpy(p, s);
//   return p;
// }
// 
// 
// int strcmp(const char *s1, const char *s2) __attribute__((section("mylib")));
// int strcmp(const char *s1, const char *s2) {
//   const char* p1 = s1;
//   const char* p2 = s2;
//   for (;; ++p1,++p2) {
//     if ((!(*p1)) && (!(*p2))) break;
//     if (*p1 != *p2) return *p1 - *p2;
//   }
//   return 0;
// }
// 
// int isupper(int c) __attribute__((section("mylib")));
// int isupper(int c) {
//   if ('A' <= c && c <= 'Z')
//     return 1;
//   else
//     return 0;
// }
// 
// 
// int toupper(int c) __attribute__((section("mylib")));
// int toupper(int c) {
//   if ('a' <= c && c <= 'z')
//     return c - 'a' + 'A';
//   return c;
// }
// 
// 
// int tolower(int c) __attribute__((section("mylib")));
// int tolower(int c) {
//   if ('A' <= c && c <= 'Z')
//     return c - 'A' + 'a';
//   return c;
// }
// 
// 
// int isalpha(int c) __attribute__((section("mylib")));
// int isalpha(int c) {
//   if ('a' <= c && c <= 'z')
//     return 1;
//   else if ('A' <= c && c <= 'Z')
//     return 1;
//   else
//     return 0;
// 
//   // return ('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z');
// }
// 
// 
// int isdigit(int c) __attribute__((section("mylib")));
// int isdigit(int c) {
//   if ('0' <= c && c <= '9')
//     return 1;
//   else
//     return 0;
//   // return ('0' <= c && c <= '9');
// }
// 
// 
// int isspace(int c) __attribute__((section("mylib")));
// int isspace(int c) {
//   if (' ' == c || '\t' == c)
//     return 1;
//   else
//     return 0;
// }
// 
// 
// void* memcpy(void *_d, const void* _s, size_t n) __attribute__((section("mylib")));
// void* memcpy(void *_d, const void* _s, size_t n) {
//   void *dest = _d;
//   char *d = (char*)_d, *s = (char*)_s;
//   for (; n; ++d,++s,--n) *d = *s;
//   return dest;
// }
// 
// 
// void* memset(void *_s, int c, size_t n) __attribute__((section("mylib")));
// void* memset(void *_s, int c, size_t n) {
//   char *s = (char*)_s;
//   for (; n; ++s,--n) *s = c;
//   return _s;
// }
// 
// 
// char* strtok(char *s, const char *delim) __attribute__((section("mylib")));
// char* strtok(char *s, const char *delim) {
//   static char* p = NULL;
//   if (s) p = s;
//   char* tok = p;
//   if (!tok) return tok;
// 
//   for (; *p; ++p) {
//     const char *d = delim;
//     for (; *d; ++d) {
//       if (*p == *d) { *p = '\0'; ++p; return tok; }
//     }
//   }
//   p = NULL;
//   if (*tok) return tok;
//   return NULL;
// }
#ifdef __cplusplus
}
#endif

