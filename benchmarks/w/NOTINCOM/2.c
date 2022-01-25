




#include<stdio.h>


int main(){

	int t,i,j,n,m,count;
	scanf("%d",&t);

	while(t--){

		scanf("%d%d",&n,&m);
		int arr[n],ptr[m];
		for(i=0;i<n;i++){
			scanf("%d",&arr[i]);
		}
		count=0;
		for(i=0;i<m;i++){
			scanf("%d",&ptr[i]);
			
		}
		printf("%d\n",count);
	}	

	return 0;

}

