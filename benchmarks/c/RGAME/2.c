




#include <stdio.h>



#define x 1000000007

int main()
{
	int t,n,i;
	long int a;
	long long int b,c,d;
	scanf("%d",&t);
	while(t--)
	{
		scanf("%d",&n);
	    scanf("%ld",&a);
		b=2*a;
		c=0;
		d=2;
		for(i=1;i<=n;i++){
			scanf("%ld",&a);
			c*=2;
			c+=b*a;
			c=c%x;
			b+=d*a;
			b%=x;
			d*=2;
			d%=x;
		}
		printf("%lld\n",c);
	}
	return 0;
}




