/*
 * @Author: lixialin 875488840@qq.com
 * @Date: 2024-03-27 11:48:26
 * @LastEditors: lixialin lixialin@nullmax.ai
 * @LastEditTime: 2024-03-27 19:44:23
 * @FilePath: /nm_tools/learning/cpp/p2_hello_world.cpp
 * @Description: 
 * 
 * Copyright (c) 2024 by Nullmax, All Rights Reserved. 
 */
#include <iostream> 
// #include是预处理器编译指令，用于引入其他文件中的代码。
// #include <iostream> 表示引入标准输入输出库中的iostream头文件，该头文件包含了标准输入输出函数的声明。
// 引入头文件后，可以使用其中的函数和类。
#include<unistd.h>
using namespace std; 
// using namespace std; 表示使用标准命名空间std中的所有标识符。
// 引入命名空间后，可以使用其中的函数和类，而不必在函数名或类名前加上命名空间名。

  
int main()
{   
    cout << "Hello, world!~" << endl;
    // cout是标准输出流对象，endl是换行符。
    // cout << "Hello, world!~" << endl; 表示输出字符串"Hello, world!~"并换行。  
    
    // system("pause");
    pause();
    // system("pause")表示执行系统命令"pause"，等待用户按下任意键后继续执行。
    // pause()表示等待用户按下任意键后继续执行。

    return 0; 
    // return 0表示程序正常退出，返回值为0。
}


// 运行cpp程序出现的bug:The preLaunchTask 'C/C++:gcc build active file' terminated with exit code-1
// 原因：gcc是针对C语言的编译器，而g++是针对C++语言的编译器。g++会自动链接STL库，所以使用gcc.exe可能无法链接c++需要的库.
// 解决方法：打开.vscode下的tasks.json文件，将"command": "/usr/bin/gcc",替换成"command": "/usr/bin/g++",

// 运行cpp程序继续出现的bug：sh: 1: pause: not found
// 解决办法：新增#include<unistd.h>，将system("pause")修改成pause()
