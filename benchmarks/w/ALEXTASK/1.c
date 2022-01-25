




#include<stdio.h>
long long int gcd(long long int x,long long int y)
{
    if(y==0)
        return x;
    else
        return(gcd(y,(x%y)));
}
 main()
{
    int t,i,j;
     long long int min;
    scanf("%d",&t);
    while(t--)
    {
        int n;
        scanf("%d",&n);
        long long int a[n];
        for(i=0;i<n;i++)
        {
            scanf("%lld",&a[i]);
        }
        min=a[0]*a[1];
        long long int lcm;
        for(i=0;i<n;i++)
        {
            for(j=i+1;j<n;j++)
            {
                lcm=(a[i]*a[j])/gcd(a[i],a[j]);
            }
        }
        if(min>lcm)
            min=lcm;


          printf("%lld\n",min);
    }
}


