




#include<stdio.h>
int gcd(int a,int b)
{
if(b==0)
return a;
else
return gcd(b,a%b);
}
int main()
{
int t;
scanf("%d",&t);
while(t--)
{
int n;
scanf("%d",&n);
long long int a[n],i,j;
for(i=0;i<n;i++)
{
scanf("%lld",&a[i]);
}
long long int min=1000000000;
for(i=0;i<n;i++)
{
for(j=i+1;j<n;j++)
{
long long int b=(a[i]*a[j]/gcd(a[i],a[j]));
if(b<min)
{
min=b;
}
}
}
printf("%lld\n",min);
}
return 0;
}


