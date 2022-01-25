




#include <stdio.h>

int main() {
    int i,j,n,k,a[100000],b[100000],c[100000],d[100000],p,min;

        scanf("%d",&n);
        scanf("%d",&k);
        for(j=0;j<=n;j++)
        {
            scanf("%d",&a[j]);
            c[j] = 0;
        }
        b[0]=a[0];
	   d[0] = -1;
	    min = 1;
        for(i=1;i<=k;i++)
	    {
	        b[i]=a[0]*a[i];
	        d[i]=0;
	        if(b[i]<b[min])
	        min = i;
	    }
	    printf("%d\n%d\n",b[min], min);

	return 0;
}



