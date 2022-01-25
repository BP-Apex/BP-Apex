




#include <stdio.h>

int main(void) {
	// your code goes here
	int t,i;
  scanf("%d",&t);
  for(i=0;i<t;i++)
  {
    int n;
    scanf("%d",&n);
    n=n-2;
    n=n/2;
    printf("%d\n",n*(n+1)/2);
    }
	return 0;

}



