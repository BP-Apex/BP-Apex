




#include <stdio.h>

int main(void) {
	// your code goes here
	int t;
	scanf("%d",&t);
	while(t--)
	{
	    int n,k,e,m,i,j,x,temp;
	    scanf("%d %d %d %d",&n,&k,&e,&m);
	    int a[n];
	    for(i=0;i<n-1;i++)
	    {
	        a[i]=0;
	        for(j=0;j<e;j++)
	        {
	            scanf("%d ",&x);
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
	    for(i=0;i<e-1;i++)
	    {
	        scanf("%d ",&x);
	        a[n-1]+=x;
	    }
	   int diff=a[k-1]-a[n-1];
	   if(diff<0)
	   diff=0;
	   if(diff<m)
	   printf("%d\n",diff);
	   else
	   printf("Impossible\n");
	}
	return 0;
}



