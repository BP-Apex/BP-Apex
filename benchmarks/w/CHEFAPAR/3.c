




#include<stdio.h>

int main()
{
	int t;
	scanf("%d",&t);
	while(t--)
	{
		long long n,amount=0,count=0,flag=0;
		scanf("%lld",&n);
		int A[n],i,j;
		for(i=0;i<n;i++)
		scanf("%d",&A[i]);

		for(i=0;i<n;i++)
		{
			if(A[i]==0)
			{
				count+=1;
				for(j=i+1;j<n;j++)
				{
					if(A[j]==1)
					flag+=1;
				}
			}
		}
		amount=amount+(count*1100)+(flag*100);
		printf("%lld\n",amount);
	}
	return 0;
}

