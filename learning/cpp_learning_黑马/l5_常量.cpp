#include<iostream>
#include<unistd.h>
#define Day 7
using namespace std;

int main()
{
    // 1.宏常量  #define Day 7
    // 2.const 修饰的变量也成为常量
    cout << "一周总共有" << Day << "天" << endl;
    const int month = 12;
    cout << "一年有" << month << "月" << endl;
    pause();
    return 0;   


}