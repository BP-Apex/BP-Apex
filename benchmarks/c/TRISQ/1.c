




#include <stdio.h>

int main(void) {
	// your code goes here
	int t;
	scanf("%d",&t);
	while(t--){
	    int base,n=0;
	    scanf("%d",&base);
	    while(base>2){
	        n=n+(base-2)/2;
	        base=base-2;
	    }
	    printf("%d\n",n);
	}
	return 0;
}



