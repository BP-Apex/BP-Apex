




#include <stdio.h>

#define M 1000000000L
#define N 1000000007L 

int main(void) {
	// your code goes here
	int k,n,i,j,a[100009],c[100009],d[100009],min;
	long long int b[100009],p;
	scanf("%d %d",&n,&k);
	for(i=0;i<n;i++)
	{ scanf("%d",&a[i]);
	  c[i]=0;
	}
	b[0]=a[0];
	d[0]=-1;
	for(i=1;i<=k;i++)
	{ b[i]=a[0]*a[i];
	  d[i]=0;
	}
	for(i=k+1;i<n;i++)
	{ j = i-k;
	  min = j;
	  for(j++;j<i;j++)
	  { if((c[j]<c[min])||(c[min]==c[j]&&b[j]<b[min]))
	     { min = j; }
	  }
	  b[i]=b[min]*a[i];
	  c[i]=c[min];
	  d[i]=min;
	  while(b[i]>M) {
	      b[i] /= 10;
	      c[i]++; }
	}
	p=a[n-1]; i=d[n-1];
	while(i>=0)
	{ p *= a[i];
	  i = d[i];
	  p %= N;
	}
	printf("%lld",p); 
	return 0;
}



