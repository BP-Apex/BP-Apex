




#include<stdio.h>
#define k 1000000007
int main()
{
    int l,n,i;
    long p;
    long long q,r,s;
    scanf("%d",&l);
    while(l--)
    {
        scanf("%d %ld",&n,&p);
        q=2*p;
        r=0;s=2;
        for(i=1;i<=n;i++){
            scanf("%ld",&p);
            r*=2;
            r+=q*p;
            q=q%k;
            r+=s*p;
            q%=k;
            s*=2;
            s%=k;
            
        }
        printf("%lld\n",r);
    }
}



