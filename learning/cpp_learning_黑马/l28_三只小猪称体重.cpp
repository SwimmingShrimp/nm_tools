/*
 * @Author: lixialin lixialin@nullmax.ai
 * @Date: 2024-04-01 19:49:52
 * @LastEditors: lixialin lixialin@nullmax.ai
 * @LastEditTime: 2024-04-01 19:56:11
 * @FilePath: /nm_tools/learning/cpp/l28_pig.cpp
 * @Description:
 * 
 * Copyright (c) 2024 by Nullmax, All Rights Reserved. 
 */
#include<iostream>
#include<unistd.h>
using namespace std;

int main()
{   
    int num1 = 0;
    int num2 = 0;
    int num3 = 0;
    cout << "请输入小猪A的体重" << endl;
    cin >> num1;
    cout << "请输入小猪B的体重" << endl;    
    cin >> num2;
    cout << "请输入小猪C的体重" << endl;    
    cin >> num3;
    cout << "小猪A的体重为：" << num1 << "kg" << endl;
    cout << "小猪B的体重为：" << num2 << "kg" << endl;
    cout << "小猪C的体重为：" << num3 << "kg" << endl;
    if(num1>num2){
        if(num1>num3){
            cout << "体重最重的是小猪A" << endl;
        }else{
            cout << "体重最重的是小猪C" << endl;
        }
    }
    else
    {
        if(num2>num3){
            cout << "体重最重的是小猪B" << endl;
        }else{
            cout << "体重最重的是小猪C" << endl;
        }
    }

    pause();
    return 0;
}