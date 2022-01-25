




#include<stdio.h>
int main(){
	int t,n;
	
	int i,j,k;
	
	scanf("%d",&t);
	for(i=0;i<t;i++){
		scanf("%d",&n);
		int A[n],A1[n],A2[n];
		for(j=0; j<n;j++){
			scanf("%d",&A[j]);
			A1[j] = A[j] / 65536;
			A2[j] = A[j] % 65536;
    }
	k = i+1;
	int p,q;
	printf("Case %d:\n",k);
	for(p = 0;p<n; p++){
		printf("%d ",A2[p]);
	}
	printf("\n");
	for(p = 0;p<n; p++){
		printf("%d ",A1[p]);
	}
	printf("\n");
	
	}
	return 0;
}

