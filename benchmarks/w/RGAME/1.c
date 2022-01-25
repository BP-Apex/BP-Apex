




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
            scanf("%d", a + i);
            for(int j = 1; j < i; j++)
                for(int k = 0; k < n - i - j; k++)
                    sum += a[i] * a[j] * 2 % MOD;
            if(i > 0)
                for(int j = 0; j <= n - i; j++)
                    sum += a[0] * a[i] * 2 % MOD;
            sum %= MOD;
        }
        printf("%d\n", sum);
    }
    
	return 0;
}



