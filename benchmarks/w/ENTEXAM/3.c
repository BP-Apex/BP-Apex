




#include <stdio.h>
main()
{
    int t;
    scanf("%d",&t);
    for(int k=0;k<t;k++)

    {
        int n,k,e,m,i,j,a[10000][5],sum[10000],max;
        scanf("%d%d%d%d",&n,&k,&e,&m);
        sum[-1]=0;
        for(i=0;i<n-1;i++)
        {
            for(j=0;j<e;j++)
            {
            scanf("%d",&a[i][j]);
            sum[i]=sum[i]+a[i][j];
            }
        }
        for(i=0;i<e-1;i++)
        scanf("%d",&a[n-1][i]);
        for(j=0; j<n-1;j++)
        {
            max=sum[j];
            for(i=j;sum[i-1]<sum[i];i++)
            {
                sum[i-1]=sum[i];
            }
            sum[i]=max;
        }
        for(i=0;i<k-1;i++)
        printf("%d\n",sum[i]+1);
    }
}



