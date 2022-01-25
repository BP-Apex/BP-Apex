




#include <stdio.h>

int main(void) 
{
    int t,n,c;
    scanf("%d",&t);
    while(t--)
    {
        scanf("%d",&n);
        c=n%8;
        if(c==1||c==4)
        {
            if(c==1)
            printf("%dLB\n",n+3);
            else
            printf("%dLB\n",n-3);
        }
        if(c==2||c==5)
        {
           if(c==2)
            printf("%dMB\n",n+3);
            else
            printf("%dMB\n",n-3);   
        }
         if(c==3||c==6)
        {
           if(c==3)
            printf("%dUB\n",n+3);
            else
            printf("%dUB\n",n-3);   
        }
         if(c==7||c==0)
        {
           if(c==7)
            printf("%dSU\n",n+1);
            else
            printf("%dSL\n",n-1);   
        }
    }
    
	// your code goes here
	return 0;
}



