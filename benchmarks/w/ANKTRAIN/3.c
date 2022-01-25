




#include<stdio.h>
int main()
{ int t,n;
  scanf("%d",&t);
  while(t--)
  { scanf("%d",&n);
     int rem=n%8;
  
   if(rem==1)
  printf("%dLB\n",n+3);
   if(rem==2)
  printf("%dMB\n",n+3);
   if(rem==3)
  printf("%dUB\n",n+3);
   if(rem==4)
  printf("%dLB\n",n-3);
   if(rem==5)
  printf("%dMB\n",n-3);
   if(rem==6)
  printf("%dUB\n",n-3);
   if(rem==7)
  printf("%dSU\n",n+1);
   if(rem==0)
  printf("%dSL\n",n+1);
  }
}

