




#include<stdio.h>
 
/*int cmpfunc (const void * a, const void * b)
{
   return ( *(long long int*)a - *(long long int*)b );
}*/
long long int sum[5][10000]={0},ans[5],marks[5][10000][4]={0},m[5];
 
int main()
{
    int t,n[5],k[5],e[5],i,j,l;
    long long int u,temp,c,min,a;
 
    scanf("%d",&t);

    for(i=0;i<t;i++)
    {
    scanf("%d%d%d%lld",&n[i],&k[i],&e[i],&m[i]);
    for(j=0;j<n[i]-1;j++)
    {
        sum[i][j] = 0;
        for(l=0;l<e[i];l++)
        {
            scanf("%lld",&marks[i][j][l]);
            sum[i][j] = sum[i][j] + marks[i][j][l];
        }
    }
    ans[i] = 0;
    for(l=0;l<e[i]-1;l++)
    {
        scanf("%lld",&marks[i][n[i]-1][l]);
        ans[i] = ans[i] + marks[i][n[i]-1][l];
    }

        for(j=0;j<n[i]-1;j++)
        {
            min = sum[i][j];
            for(l=j;l<n[i]-1;l++)
            {
                if(min >= sum[i][l])
                {
                    min = sum[i][l];
                    c = l;
                }
            }
            temp = sum[i][j];
            sum[i][j] = min;
            sum[i][c] = temp;
        }

        a = n[i] - k[i] - 1;
        u = sum[i][a] - ans[i];
 
        if(u >= m[i])
        {
            printf("Impossible\n");
        }
        else if(u < 0)
        {
            u = 0;
            printf("%lld\n",u);
        }
        else
        {
            u=u+1;
            printf("%lld\n",u);
        }
    }

    return 0;
}
 

