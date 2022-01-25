




#include <stdio.h>

int main(void) {
	// your code goes here
	int t;
	scanf("%d",&t);
	while(t--)
	{
	    long int n,i,ad=0,c1=0,c0=0;
	    scanf("%ld",&n);
	    int a[n];
	    for(i=1;i<=n;i++)
	        scanf("%d",&a[i]);
	    for(i=1;i<=n;i++)
	    {
	        if(a[i]==1)
	            c1++;
	        else
	            c0++;
	    }
	    ad=c0*1100;
	    if(a[1]!=1)
	        ad+=c1*100;
	    printf("%ld\n",a);
	   
	}
	return 0;
}



