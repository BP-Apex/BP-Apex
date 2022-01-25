




#include <stdio.h>

int main(void) {
	// your code goes here
	int t;
	scanf("%d",&t);
	while(t--)
	{
	    long long int n,k,e,m,i,j,x,temp;
	    scanf("%lld %lld %lld %lld",&n,&k,&e,&m);
	    long long int a[n];
	    for(i=0;i<n-1;i++)
	    {
	        a[i]=0;
	        for(j=0;j<e;j++)
	        {
	            scanf("%lld ",&x);
	            a[i]+=x;
	        }
	    }
	    for(i=0;i<n-2;i++)
	    {
	        for(j=i+1;j<n-1;j++)
	        {
	            if(a[j]>a[i])
	            {
	            temp=a[i];
	            a[i]=a[j];
	            a[j]=temp;
	            }
	        }
	    }
	    a[n-1]=0;
	    for(i=0;i<e-1;i++)
	    {
	        scanf("%lld ",&x);
	        a[n-1]+=x;
	    }
	   // printf("%d %d\n",a[k-1],a[n-1]);
	   long long int diff=a[k-1]-a[n-1]+1;
	   if(diff<0)
	   diff=0;
	   if(diff<=m)
	   printf("%lld\n",diff);
	   else
	   printf("Impossible\n");
	}
	return 0;
}



