




#include <stdio.h>
int gcd(int a,int b)
{
	if(a==0)
	return b;
	return gcd(b%a,a);
}
int main(void) {
int t,n,a[500];
scanf("%d",&t);
while(t--)
{
	scanf("%d",&n);
	int c,b;
	for(int i=0;i<n;i++)
	{
		scanf("%d",&a[i]);
	}
		int max=0;
	for(int j=0;j<n;j++)
	{
		for(int k=j+1;k<n;k++)
		{


			if(	gcd(a[j],a[k])>max)
		{   c=a[j];
		    b=a[k];
			max=gcd(a[j],a[j+1]);

		}
		}
	}

int result=(b*c)/max;
printf("%d\n",result);

}
	return 0;
}


