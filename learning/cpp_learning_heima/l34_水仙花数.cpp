#include<iostream>
#include<unistd.h>
using namespace std;
// 水仙花数，一个3位数的数，每个位上的数字的3次幂之和等于它本身
// 153 = 1^3 + 5^3 + 3^3
int main()
{
    // 1. 将所有的3位数进行输出
    int num = 100;
    do{ 
        int a=0;
        int b=0;
        int c=0;
        a = num%10;
        b = num/10%10;
        c = num/100%10;
        if(num==a*a*a+b*b*b+c*c*c)
        {
            cout<<num<<endl;    
        }
        num++;
    }
    while(num<999);
    // 2. 判断它是否为水仙花数
    // 3. 如果是，输出
    // 4. 否则，不输出
}