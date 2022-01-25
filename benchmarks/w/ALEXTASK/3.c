




#include<stdio.h>

unsigned  long long int hcf(unsigned long long int a, unsigned long long int b){
	if(b==0) return a;
	else hcf(b,a%b);
}

int main(){
	int T;
	scanf("%d",&T);
	while(T--){
		int N;
		scanf("%d",&N);
		int i,j;
		unsigned long long int rd_t[N],t=999999999999999999,gcd,lcm,rstt;
		for(i=0;i<N;i++)
			scanf("%llu",&rd_t[i]);
		for(i=0;i<N;i++){
			for(j=i+1;j<N;j++){
				if(rd_t[i]<t && rd_t[j]<t){
					gcd=hcf(rd_t[i],rd_t[j]);
					lcm=(rd_t[i]*rd_t[j])/gcd;
					if(lcm<t) t=lcm;
				}
			}
		}
		printf("%llu",t);
	}
	return 0;
}

