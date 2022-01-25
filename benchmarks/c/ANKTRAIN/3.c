




#include<stdio.h>
int main()
{
    int t;
    scanf("%d",&t);
    while(t--)
    {
        int n,a,b;
        scanf("%d",&n);
        a = n%8;
        b = n/8;
        if(a==1)
        {
            printf("%dLB\n",(b*8 + 4));
        }
        if(a==2)
        {
            printf("%dMB\n",(b*8 + 5));
        }
        if(a==3)
        {
            printf("%dUB\n",(b*8 + 6));
        }
        if(a==4)
        {
            printf("%dLB\n",(b*8 + 1));
        }
        if(a==5)
        {
            printf("%dMB\n",(b*8 + 2));
        }
        if(a==6)
        {
            printf("%dUB\n",(b*8 + 3));
        }
        if(a==7)
        {
            printf("%dSU\n",((b+1)*8));
        }
        if(a==0)
        {
            printf("%dSL\n",((b-1)*8 + 7));
        }
    }
    return 0;
}





