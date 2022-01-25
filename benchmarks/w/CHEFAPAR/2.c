




#include<stdio.h>
int main()
{
	long t,n,i,s,flag,j;
	scanf("%ld",&t);
	while(t--)
	{
		s=0;
		flag=1;
		scanf("%ld",&n);
		long a[n];
		for(i=0;i<n;i++)
		{
			scanf("%ld",&a[i]);
		}
		for(i=0;i<n;i++)
		{
			if(a[i]==0)
			{
				s=s+1100;
				flag=0;
			}
			if(a[i]==1&&flag==0)
			{
				s=s+100;
				flag=1;
			}
			if(a[i]==1&&flag==1)
			{
				s=s+0;
				flag=1;
			}
		}
		printf("%ld\n",s);
	}
	return(0);
}

