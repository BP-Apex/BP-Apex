




#include<stdio.h>
long long int find(long long int x,long long int parent[])
{
	if(parent[x]==x)
	return x;
	parent[x]=find(parent[x],parent);
}
int main()
{
	long long int s[100005],n,q,x,y,decide,i;
    scanf("%lld",&n);
    long long int parent[100005];
    for( i=1;i<=n;i++)
    {
        scanf("%lld",&s[i]);
    }
    for(i=1;i<=n;i++)
    {
        parent[i]=i;
    }
    scanf("%lld",&q);
    while(q--)
    {
        scanf("%lld",&decide);
        if(decide==1)
        {
            scanf("%lld",&x);
            long long int ans=find(x,parent);
            printf("%lld\n",ans);
        }
        else
        {
            scanf("%lld %lld",&x,&y);
            x=find(x,parent);
            y=find(y,parent);
            if(x==y)
            {
                printf("Invalid query!\n");
            }
            else if(s[x]<s[y])
            {
                parent[x]=y;
            }
            else if(s[x]>s[y])
            {
                parent[y]=x;
            }
        }
    }
	return 0;
}

