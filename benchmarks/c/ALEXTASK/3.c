





    #include <stdio.h>

    unsigned long long hcf(unsigned long long a, unsigned long long b)
        {
        if(b==0)
            return a;
        else
            return hcf(b, a%b);
    }

    int main() {
        int t, n, i, j;
        scanf("%d", &t);
        while(t--)
            {
            scanf("%d", &n);
            unsigned long long a[n], min=999999999999999999, lcm;
            for(i=0; i<n; i++)
                scanf("%llu", &a[i]);
            for(i=0; i<n; i++)
                {
                for(j=i+1; j<n; j++)
                    {
                    if(a[i]>min||a[j]>min) continue;
                    lcm=((a[i]*a[j])/(hcf(a[i], a[j])));
                    if(min>lcm) min=lcm;
                }
            }
            printf("%llu\n", min);
        }
    }


