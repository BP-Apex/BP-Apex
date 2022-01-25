




#include<stdio.h>
int main()
{
    long long int num,i,t,a,n,a1[10000],a2[10000],x,y;
    scanf("%lld",&t);
    while(t--)
    {
        scanf("%lld",&y);
        for(i=0;i<y;i++)
        {
            scanf("%lld",&num);
            a2[i]=num/65536;
            a1[i]=num-65536*a2[i];
        }
        for(i=0;i<y;i++)
            printf("%lld ",a1[i]);
        printf("\n");
        for(i=0;i<y;i++)
            printf("%lld ",a2[i]);
    }
    return 0;
}


