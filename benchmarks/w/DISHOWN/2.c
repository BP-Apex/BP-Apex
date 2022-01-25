




 #include<stdio.h>
        int find_chef(int chef[],int dish_no)
        {
            if(chef[dish_no]!=dish_no)
                chef[dish_no]=find_chef(chef,chef[dish_no]);
            return chef[dish_no];    
        }
        void allot_chef(int score[],int chef[],int x,int y)
        {
            int chef_x=find_chef(chef,x);
            int chef_y=find_chef(chef,y);
            if(chef_x==chef_y)
               printf("%s\n","Invalid query!");
            else if(score[chef_x]<score[chef_y])
                chef[chef_x]=chef_y;
            else if(score[chef_x]>score[chef_y])
                chef[chef_y]=chef_x;
        }
        int main()
        {
            int n,query,i,j;
            scanf("%d",&n);
            int score[n+1],chef[n+1];
            for(j=0;j<=n;j++)
            {
                chef[j]=j;

            }
            for(i=1;i<=n;i++)
            {
                scanf("%d",&score[i]);

            }
            int x,y,z;
            scanf("%d",&query);
            while(query--)
            {
                int task;
                scanf("%d",&task);
                if(task==0)
                {

                    scanf("%d %d",&x,&y);
                    allot_chef(score,chef,x,y);
                }
                else if(task==1)
                {

                    scanf("%d",&z);
                    printf("%d",find_chef(chef,z));

                }
            }
            return 0;
        }  

