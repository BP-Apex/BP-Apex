




#include <stdio.h>

int main(){
	int t, n, i, d, c, p, s;
	scanf("%d", &t);
	while(t--){
		scanf("%d", &n);
		c=0;	p=n;	s=0;
		for(i=0; i<n; i++){
			scanf("%d", &d);
			if(d==0){
				c++;
				if(c==1)
					p=i;
			}
		}
		s=c*1000+(n-p)*100;
		printf("%d\n", s);
	}
	return 0;
}

