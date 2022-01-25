




#include <stdio.h>

int main()
{
int i,t;
scanf("%d",&t);
while(t--)
{
    int b,s=0;
    scanf("%d",&b);
    while(b>0)
    {
        s=s+((b/2)-1);
        b=b-2;

    }
    printf("%d\n",s);
}
    return 0;
}


