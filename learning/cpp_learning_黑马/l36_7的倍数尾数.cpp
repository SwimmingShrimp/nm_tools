#include<iostream>
using namespace std;
#include<unistd.h>

int main()
{
    // 1.先输出0-100
    // 2.找到特殊的数字，并输出
    for(int num=1;num<=100;num++)
    {
        int a=0;
        int b=0;
        int c=0;
        a = num - num/10*10;
        b = num/10 - num/100*10;
        c = num%7;
        if(a==7 || b==7 || c==0)
        {
            cout<<num<<endl;
        }
    }

}