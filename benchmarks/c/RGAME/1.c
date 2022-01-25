




#include <stdio.h>

#define MOD 1000000007

int main(void) {
	int t;
	
	scanf("%d", &t);
    
    while(t--) {
        int n;
        scanf("%d", &n);
        
        long long int a[n + 1], sum = 0;
        for(int i = 0; i < n + 1; i++) {
            scanf("%lld", a + i);
            for(int j = 1; j < i; j++) {
                long long int tmp = a[i] * a[j];
                for(int k = 0; k < n - i + j; k++)
                    tmp = (tmp << 1) % MOD;
                sum += tmp;
            }
            if(i > 0) {
                long long int tmp = a[0] * a[i];
                for(int j = 0; j <= n - i; j++)
                    tmp = (tmp << 1) % MOD;
                sum += tmp;
            }
            sum %= MOD;
        }
        printf("%lld\n", sum);
    }
    
	return 0;
}



