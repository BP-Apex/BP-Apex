




#include<stdio.h>
int main()
{
	int t;
	//printf("enter size\n\t");
	scanf("%d",&t);
	while(t--)
	{
		int i,j,n,m;
		//printf("enter value for N & M \n\t");
		scanf("%d%d",&n,&m);
		int a[n],b[m];
		for(i=0;i<n;i++)
		{
			scanf("%d",&a[i]);
		}
		for(i=0;i<m;i++)
		{
			scanf("%d",&b[i]);
		}

		int k=0;
		for(i=0;i<n;i++)
		{
			for(j=0;j<m;j++)
			{
				if(a[i]==a[j])
				{
					k++;
				}
			}
		}

		printf("%d",k);
	}
}


