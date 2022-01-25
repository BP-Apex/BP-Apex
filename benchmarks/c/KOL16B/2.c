




#include <stdio.h>

int main(void) {
    int t, casenum = 1;
    
    for (scanf("%d", &t); t; t--) {
        int n, a[10001], b[10001], i;
        
        scanf ("%d", &n);
        
        for (i = 0; i < n; i++) {
            scanf ("%d", &a[i]);
            b[i] = a[i] / 65536;
            a[i] = a[i] % 65536;
        }

        printf ("Case %d:\n", casenum++);
        for (i = 0; i < n; i++) {
            printf ("%d ", a[i]);
        }
        
        printf ("\n");
        for (i = 0; i < n; i++) {
            printf ("%d ", b[i]);
        }
        
        printf ("\n");
    }
	return 0;
}

