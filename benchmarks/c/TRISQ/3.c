




#include <stdio.h>

int main(void) {
    int a,b,c;
    scanf ("%d",&b);
    for (int i=0;i<b;i++) {
        scanf ("%d",&a);
        a=a/2;
        a=a-1;
        for (int j=1;j<=a;j++) {
            c=c+j;
        }
        printf ("%d\n",c);
        c=0;
    }
	return 0;
}



