




#include<stdio.h>
#include<limits.h>
int gcd(int a, int b)
{
    if(a == 0)
        return b;
    return gcd(b%a, a);
}
int main()
{
	int t;
	scanf("%d", &t);
	while(t--)
	{
		int i, j, n;
		scanf("%d", &n);
		long long a[n];
		for(i=0; i<n; i++)
			scanf("%lld", &a[i]);
		int min = INT_MAX;
		for(i=0; i<n-1; i++)
			for(j=i+1; j<n; j++)
				if((a[i]*a[j])/gcd(a[i], a[j]) < min)
					min = (a[i]*a[j])/gcd(a[i], a[j]);
		printf("%d\n", min);

	}
}

