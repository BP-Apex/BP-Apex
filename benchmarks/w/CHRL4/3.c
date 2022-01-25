




#include <stdio.h>

int main(void) {
	int n,k;
	scanf("%d %d\n",&n,&k);
	int arr[n];
	int i=0;
	for(i=0;i<n;i++)
	{
	    scanf("%d",&arr[i]);
	}
	int t=n-1,pro=1;
	while(t>=k)
	{
	    pro=pro*arr[t-k];
	    t=t-k;
	}
	printf("%d",pro);
	return 0;
}



