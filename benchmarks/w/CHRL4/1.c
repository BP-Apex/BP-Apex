




#include <stdio.h>


int main(void) {
	// your code goes here
	int n,k,a[100009],i,j,min,b[100009];
	long long int p;
	scanf("%d %d",&n,&k);
	for(i=0;i<n;i++)
	      scanf("%d",&a[i]);
	b[0]=-1;
	for(i=1;i<=k;i++)
	  b[i]=0;
	for(i=k+1;i<n;i++)
	  { j = i-k;
	    min = j;
	    for(;j<i;j++)
	     if(a[j]<a[min]) min = j;
	    b[i]=min;
	  }
	p= a[n-1];
	for(i=b[n-1];i>=0;i=b[i]) ;
	{ p *= a[i];
	    p %=1000000007L;
    }

	printf("%lld",p);
	return 0;
}



