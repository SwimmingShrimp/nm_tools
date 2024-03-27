/*
 * @Author: lixialin 875488840@qq.com
 * @Date: 2024-03-27 11:48:26
 * @LastEditors: lixialin 875488840@qq.com
 * @LastEditTime: 2024-03-27 11:57:09
 * @FilePath: /nm_tools/learning/cpp/p2_hello_world.cpp
 * @Description: 
 * 
 * Copyright (c) 2024 by Nullmax, All Rights Reserved. 
 */
#include <iostream>
#include<unistd.h>
using namespace std; 


int main()

{   
    cout << "Hello, world!~" << endl;
    
    // system("pause");
    pause();

    return 0; 
    
}


// 运行cpp程序出现的bug:The preLaunchTask 'C/C++:gcc build active file' terminated with exit code-1
// 原因：gcc是针对C语言的编译器，而g++是针对C++语言的编译器。g++会自动链接STL库，所以使用gcc.exe可能无法链接c++需要的库.
// 解决方法：打开.vscode下的tasks.json文件，将"command": "/usr/bin/gcc",替换成"command": "/usr/bin/g++",

// 运行cpp程序继续出现的bug：sh: 1: pause: not found
// 解决办法：新增#include<unistd.h>，将system("pause")修改成pause()
