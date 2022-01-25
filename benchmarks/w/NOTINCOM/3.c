




#include<stdio.h>
int main()
{
    int t;
    scanf("%d",&t);
    while(t--)
    {
        int n,m;
        int c=0;
        scanf("%d%d",&n,&m);
        int A[10000];int B[10000];
        for(int i=0;i<n;i++)
        {
            scanf("%d",&A[i]);
        }
        for(int j=0;j<m;j++)
        {
            scanf("%d",&B[j]);
        }

        for(int k=0;k<n;k++)
        {
            for(int h=0;h<m;h++)
            {
                if(A[k]==B[k])
            {
                c++;
                break;
            }
            }
        }

        printf("%d\n",c);
    }
    return 0;
}


