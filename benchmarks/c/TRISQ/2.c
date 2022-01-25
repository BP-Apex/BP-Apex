




#include <stdio.h>

int main(void) {
	// your code goes here
	int t;
	scanf("%d",&t);
	int k;
	int count;
	for(k=1;k<=t;k++)
	{
	    count=0;
	    int i,j,b;
	    scanf("%d",&b);
	    for(i=2;i<=b-2;)
	    {
	        for(j=2;j<=b-i;)
	        {
	            count++;
	            j+=2;
	        }
	        i+=2;
	    }
	    printf("%d\n",count);
	}
	return 0;
}



