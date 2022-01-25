




#include<stdio.h>
#define MAX 100000
int main()
{

    int test,n,i,flag,count,due,rem;
    scanf("%d",&test);
    printf("\n");
    while (test--)
    {
            count=0;
            rem=0;
            flag=0;
            scanf("%d",&n);
            int p[n];
            for (i=0;i<n;i++)
                scanf("%d",&p[i]);
            for (i=0;i<n;i++)
            {
                if (flag==0)
                {


                if (p[i]==0){flag=1;
                rem=i;
                }}
                if (p[i]==1)count++;
            }
            if (flag==0)rem=n;
            due=(n-count)*1000+(n-rem)*100;
            printf("\n%d",due);
                }
                return 0;
}


